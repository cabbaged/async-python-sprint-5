from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from models.user import User as UserModel
from schemas.user_schema import User, UserCreate
from services.password_manager import PasswordManager

test_client = TestClient(app)


@pytest.fixture
def mock_password_manager():
    return MagicMock(spec=PasswordManager)


@pytest.mark.asyncio
async def test_register_success(mock_password_manager):
    with patch("api.auth.auth.user_crud", AsyncMock()) as user_crud_mock:
        user_data = {"username": "test_user", "password": "test_password"}
        user_create_data = UserCreate(username=user_data["username"], hashed_password="hashed_password")
        user_crud_mock.create.return_value = user_create_data
        user_crud_mock.get.return_value = None  # not registered

        response = test_client.post("/api/register/", json=user_data)

        assert response.status_code == 200
        assert response.json() == {"username": user_data["username"]}


@pytest.mark.asyncio
async def test_register_existing_user(mock_password_manager):
    with patch("api.auth.auth.user_crud", AsyncMock()) as user_crud_mock:
        user_data = {"username": "existing_user", "password": "test_password"}
        user_crud_mock.get.return_value = UserModel(
            username=user_data["username"],
            hashed_password=PasswordManager.create().hash_password("test_password")
        )
        response = test_client.post("/api/register/", json=user_data)

        assert response.status_code == 400


@pytest.mark.asyncio
async def test_authenticate_success(mock_password_manager):
    with patch("api.auth.auth.user_crud", AsyncMock()) as user_crud_mock:
        user_data = {"username": "test_user", "password": "test_password"}

        user_crud_mock.get.return_value = UserModel(
            username=user_data["username"],
            hashed_password=PasswordManager.create().hash_password("test_password")
        )

        mock_password_manager.verify_password.return_value = True

        response = test_client.post("/api/auth/", json=user_data)

        assert response.status_code == 200
        assert "access_token" in response.json()
