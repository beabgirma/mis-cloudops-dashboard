from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    # Verify the dashboard loads successfully as an HTML page
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # Check that a signature element from your dashboard template is inside the page
    assert "Dashboard" in response.text