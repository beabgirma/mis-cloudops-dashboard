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