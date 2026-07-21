from fastapi.testclient import TestClient
from app.main import app
from app.repositories import service_repo
import time
from unittest.mock import patch, AsyncMock, MagicMock


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
    assert "created_at" in data
    assert "updated_at" in data

    assert data["id"] == 1
    assert data["name"] == "Email Server"
    assert data["owner"] == "MIS Team"
    assert data["status"] == "unknown"
    assert data["created_at"]== data["updated_at"]


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

    created_data = create_response.json()
    service_id = created_data["id"]
    original_created_at = created_data["created_at"]
    original_updated_at = created_data["updated_at"]
    time.sleep(0.01)
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
    assert data["created_at"] == original_created_at
    assert data["updated_at"] != original_updated_at


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

def test_get_service_by_id_not_found():
    response = client.get("/services/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_delete_service_by_id():
    response=client.post(
        "/services",
        json={
            "name":"Network Server",
            "url" : "https://mail.example.com",
            "owner": "MIS Team"
        }
    )
    service_id = response.json()["id"]
    response=client.delete(
        f"/services/{service_id}"
    )
    assert response.status_code==200
    data =response.json()
    assert data["id"]== service_id


def test_delete_service_by_id_not_found():
    response=client.delete("/services/999")
    assert response.status_code==404
    assert response.json()["detail"]=="Service not found"



def test_trigger_health_check_not_found():
    response=client.post("/services/9999/check")
    assert response.status_code==404
    assert response.json()["detail"]=="Service not found"


def test_trigger_health_check_online():
    response=client.post(
        "/services",
        json={
            "name":"Network Server",
            "url" : "https://mail.example.com",
            "owner": "MIS Team"
        }
    )
    service_id=response.json()["id"]
    # 1. Start the patch with a standard 'with' block
    with patch("app.services.service_service.httpx.AsyncClient") as mock_client_class:
        mock_client = mock_client_class.return_value
        
        # This mocks the async context manager 'async with'
        mock_client.__aenter__.return_value = mock_client
        
        # This mocks the awaitable '.get()' call and makes it return status 200
        mock_client.get = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_client.get.return_value = mock_response

        # 2. Trigger the check inside this 'with' block
        check_response = client.post(f"/services/{service_id}/check")

        # 3. Assertions
        assert check_response.status_code == 200
        assert check_response.json()["status"] == "online"
    
def test_trigger_health_check_offline():
    response = client.post(
        "/services",
        json={
            "name": "Failing Server",
            "url" : "https://broken.example.com",
            "owner": "MIS Team"
        }
    )
    service_id = response.json()["id"]

    with patch("app.services.service_service.httpx.AsyncClient") as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.__aenter__.return_value = mock_client
        
        mock_client.get = AsyncMock()
        mock_response = AsyncMock()
        # Simulate a server failure (e.g., 500 Internal Server Error)
        mock_response.status_code = 500
        mock_client.get.return_value = mock_response

        check_response = client.post(f"/services/{service_id}/check")

        assert check_response.status_code == 200
        assert check_response.json()["status"] == "offline"