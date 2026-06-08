from fastapi.testclient import TestClient
from app.main import app
from app.repositories import service_repo

client = TestClient(app)


def setup_function():
    service_repo.reset_services()


def test_create_service():
    response = client.post(
        "/services",
        json={
            "name": "Email Server",
            "url": "https://mail.example.com",
            "owner": "MIS Team"
        }
    )
    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Email Server"
    assert data["owner"] == "MIS Team"
    assert data["status"] == "unknown"


def test_list_services():
    client.post(
        "/services",
        json={
            "name": "HR Portal",
            "url": "https://hr.example.com",
            "owner": "HR Department"
        }
    )
    response = client.get("/services")
    assert response.status_code == 200
    data = response.json()
    assert len(data["services"]) == 1
    assert data["services"][0]["name"] == "HR Portal"

def test_update_service_status():
    create_response = client.post(
        "/services",
        json={
            "name": "Email Server",
            "url": "https://mail.example.com",
            "owner": "MIS Team"
        }
    )

    service_id = create_response.json()["id"]
    response = client.patch(
        f"/services/{service_id}/status",
        json={
            "status": "online"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id
    assert data["status"] == "online"

def test_update_service_status_not_found():
    response=client.patch(
        "/services/999/status",
        json={
            "status":"offline"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"]=="Service not found"

def test_check_invalid_status():
    response=client.patch(
        "/services/1/status",
        json={
            "status":"banana"
        }
    )
    assert response.status_code==422

def test_valid_service_by_id():
    response=client.post(
        "/services",
        json={
            "name":"HR server",
            "url" : "https://mail.example.com",
            "owner":"MIS team"       
        }
    )
    service_id=response.json()["id"]
    response=client.get(
        f"/services/{service_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id
    assert data["name"] == "HR server"

"""1. Send GET request to /services/999
2. Expect status code 404
3. Expect detail to be "Service not found"""

def test_get_service_by_id_not_found():
    response = client.get("/services/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"