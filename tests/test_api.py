"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal, engine
from src.models import Base, User, Voice, Plan, Gender
from src.auth import generate_api_key, hash_api_key


@pytest.fixture(scope="module")
def test_db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def admin_user(test_db):
    """Create admin user for testing."""
    db = SessionLocal()
    api_key = generate_api_key()
    
    user = User(
        name="Test Admin",
        email="admin@test.com",
        api_key_hash=hash_api_key(api_key),
        plan=Plan.ENTERPRISE,
        quota_seconds=36000,
        used_seconds=0,
        is_active=True,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return {"user": user, "api_key": api_key}


@pytest.fixture
def test_voice(test_db):
    """Create test voice."""
    db = SessionLocal()
    
    voice = Voice(
        friendly_name="test-voice",
        minimax_voice_id="test_voice_id",
        language="en-US",
        gender=Gender.MALE,
        description="Test voice",
        is_cloned=False,
        is_active=True,
    )
    
    db.add(voice)
    db.commit()
    db.refresh(voice)
    db.close()
    
    return voice


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_unauthorized(client):
    """Test creating user without auth."""
    response = client.post(
        "/admin/users",
        json={"name": "Test", "email": "test@test.com", "plan": "basic"}
    )
    assert response.status_code == 401


def test_create_user_authorized(client, admin_user):
    """Test creating user with admin credentials."""
    response = client.post(
        "/admin/users",
        headers={"Authorization": f"Bearer {admin_user['api_key']}"},
        json={"name": "New User", "email": "newuser@test.com", "plan": "basic"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "api_key" in data
    assert data["user"]["email"] == "newuser@test.com"
    assert data["user"]["plan"] == "basic"
    assert data["user"]["quota_seconds"] == 3600


def test_list_voices_unauthorized(client):
    """Test listing voices without auth."""
    response = client.get("/v1/voices")
    assert response.status_code == 401


def test_list_voices_authorized(client, admin_user, test_voice):
    """Test listing voices with auth."""
    response = client.get(
        "/v1/voices",
        headers={"Authorization": f"Bearer {admin_user['api_key']}"}
    )
    
    assert response.status_code == 200
    voices = response.json()
    assert len(voices) > 0
    assert voices[0]["friendly_name"] == "test-voice"


def test_get_user_info(client, admin_user):
    """Test getting current user info."""
    response = client.get(
        "/v1/me",
        headers={"Authorization": f"Bearer {admin_user['api_key']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["plan"] == "enterprise"


def test_invalid_api_key(client):
    """Test with invalid API key."""
    response = client.get(
        "/v1/me",
        headers={"Authorization": "Bearer invalid_key_here"}
    )
    assert response.status_code == 401


def test_missing_authorization_header(client):
    """Test without Authorization header."""
    response = client.get("/v1/me")
    assert response.status_code == 401
