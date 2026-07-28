import asyncio
import httpx
from app.repositories.service_repo import list_service_records
from app.redis_client import send_redis_command

async def ping_and_cache_service(service_id: int, url: str):
    """Pings a service URL and catches firewall challenges explicitly for the AU presentation."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
        try:
            response = await client.get(url, headers=headers, follow_redirects=True)
            
            # Extract server signature from headers safely
            server_header = response.headers.get("server", "").lower()
            
            # If it's a security block OR the gateway explicitly identifies as Cloudflare
            if response.status_code in [400, 403, 503] and "cloudflare" in server_header:
                status = "Protected"
            else:
                status = "Healthy" if 200 <= response.status_code < 400 else "Unhealthy"
                
        except (httpx.RequestError, httpx.HTTPStatusError):
            status = "Unhealthy"

    send_redis_command(f"SET service:{service_id}:status {status}")
    send_redis_command(f"EXPIRE service:{service_id}:status 45")

async def monitor_services_loop():
    """Infinitely runs health check cycles every 30 seconds."""
    while True:
        db_services = list_service_records()
        tasks = []
        for service in db_services:
            url = getattr(service, 'url', None) or (service.get('url') if isinstance(service, dict) else None)
            s_id = getattr(service, 'id', None) or (service.get('id') if isinstance(service, dict) else None)
            
            if url and s_id:
                tasks.append(ping_and_cache_service(s_id, url))
                
        if tasks:
            await asyncio.gather(*tasks)
            
        await asyncio.sleep(30)