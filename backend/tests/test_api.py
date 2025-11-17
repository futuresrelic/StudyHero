import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, SessionLocal
from models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestAuthAPI:
    """Tests for authentication endpoints"""

    def test_register_user(self):
        """Test user registration"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword123",
                "full_name": "Test User",
                "school_level": "high"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"

    def test_login_user(self):
        """Test user login"""
        # First register
        client.post(
            "/auth/register",
            json={
                "email": "login@example.com",
                "password": "testpassword123"
            }
        )

        # Then login
        response = client.post(
            "/auth/login",
            json={
                "email": "login@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

    def test_get_current_user(self):
        """Test getting current user info"""
        # Register and get token
        reg_response = client.post(
            "/auth/register",
            json={
                "email": "currentuser@example.com",
                "password": "testpassword123"
            }
        )
        token = reg_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "currentuser@example.com"


class TestHomeworkAPI:
    """Tests for homework endpoints"""

    @pytest.fixture
    def auth_token(self):
        """Get auth token for tests"""
        response = client.post(
            "/auth/register",
            json={
                "email": f"hwtest{pytest.test_counter}@example.com",
                "password": "testpassword123"
            }
        )
        pytest.test_counter = getattr(pytest, 'test_counter', 0) + 1
        return response.json()["access_token"]

    def test_homework_history(self, auth_token):
        """Test getting homework history"""
        response = client.get(
            "/homework/history",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "scans" in data
        assert "total" in data


class TestProgressAPI:
    """Tests for progress endpoints"""

    @pytest.fixture
    def auth_token(self):
        """Get auth token for tests"""
        response = client.post(
            "/auth/register",
            json={
                "email": f"progress{pytest.test_counter}@example.com",
                "password": "testpassword123"
            }
        )
        pytest.test_counter = getattr(pytest, 'test_counter', 0) + 1
        return response.json()["access_token"]

    def test_get_progress(self, auth_token):
        """Test getting user progress"""
        response = client.get(
            "/progress/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "current_streak" in data
        assert "total_questions_solved" in data
        assert "level" in data

    def test_log_study_time(self, auth_token):
        """Test logging study time"""
        response = client.post(
            "/progress/log-study-time",
            params={"minutes": 30},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_minutes"] >= 30


# Cleanup
pytest.test_counter = 0
