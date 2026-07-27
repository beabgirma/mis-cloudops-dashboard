import pytest
from app.database import init_db

@pytest.fixture(autouse=True, scope="session")
def setup_database():
    init_db()