import asyncio
import httpx
from app.repositories.service_repo import list_service_records
from app.redis_client import send_redis_command

async def ping_and_cache_service(service_id: int, url: str):
    """Pings a service URL and stores the status in Mini Redis with a 45s TTL."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            # Match the dashboard's expected UI strings: "Healthy" or "Unhealthy"
            status = "Healthy" if 200 <= response.status_code < 300 else "Unhealthy"
        except (httpx.RequestError, httpx.HTTPStatusError):
            status = "Unhealthy"

    # Match the dashboard's expected Redis key format: service:{id}:status
    send_redis_command(f"SET service:{service_id}:status {status}")
    send_redis_command(f"EXPIRE service:{service_id}:status 45")

async def monitor_services_loop():
    """Infinitely runs health check cycles every 30 seconds."""
    while True:
        db_services = list_service_records()
        
        # Concurrently fire pings to all configured URLs
        tasks = []
        for service in db_services:
            # Handle both object attributes and dictionary formats safely
            url = getattr(service, 'url', None) or (service.get('url') if isinstance(service, dict) else None)
            s_id = getattr(service, 'id', None) or (service.get('id') if isinstance(service, dict) else None)
            
            if url and s_id:
                tasks.append(ping_and_cache_service(s_id, url))
                
        if tasks:
            await asyncio.gather(*tasks)
            
        await asyncio.sleep(30)