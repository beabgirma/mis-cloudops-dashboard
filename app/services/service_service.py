from app.repositories import service_repo
import httpx
import asyncio


def create_service(service):
    return service_repo.create_service_record(service)


def list_services():
    return {
        "services": service_repo.list_service_records()
    }


def update_service_status(service_id:int, update):
    return service_repo.update_service_status_record(
        service_id,
        update.status
    )

def get_service_by_id(service_id:int):
    return service_repo.get_service_by_id(
        service_id
    )

def delete_service_by_id(service_id:int ):
    return service_repo.delete_service_by_id(
        service_id
    )

async def check_health(service_id: int):
    service = service_repo.get_service_by_id(service_id)

    if service is None:
        return None

    try:
        async with httpx.AsyncClient() as client:
            response= await client.get(service["url"])
            if response.status_code < 300:
                status = "online"
            else:
                status = "offline"

    except:
        status = "offline"

    return service_repo.update_service_status_record(
        service_id,
        status
    )

async def periodic_health_checks():
    while True:
        tasks = []
        services = service_repo.get_all_services()
        for service in services:
            tasks.append(check_health(service["id"]))
        if tasks:
            await asyncio.gather(*tasks)
        await asyncio.sleep(60)
