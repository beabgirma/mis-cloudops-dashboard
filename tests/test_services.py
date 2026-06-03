from fastapi.testclient import TestClient
from app import main

client=TestClient(main.app)

def setup_function():
    main.services.clear()
    main.next_service_id=1

def test_create_service():
    response =client.post(
        "/services",
        json={
            "name": "Email Server",
            "url": "https://mail.example.com",
            "owner": "MIS Team"
        }
    )
    assert response.status_code==201
    data=response.json()

    assert data["id"]==1
    assert data["name"]=="Email Server"
    assert data["owner"]=="MIS Team"
    assert data["status"]=="unknown"

def test_list_services():
    
    client.post(
        "/services",
        json={
            "name": "HR Portal",
            "url": "https://hr.example.com",
            "owner": "HR Department"
        }
    )
    response=client.get("/services")
    assert response.status_code==200
    data =response.json()
    assert len(data["services"])==1
    assert data["services"][0]["name"]== "HR Portal"