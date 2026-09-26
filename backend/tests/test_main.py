
import pytest
from fastapi.testclient import TestClient

from backend.app import database
from backend.app.main import app


TEST_DEVICE = {
    "device_id": "test-device-001",
    "hostname": "PATCHOPS-TEST",
    "operating_system": "Windows",
    "os_version": "10.0.26200",
    "os_release": "11",
    "architecture": "AMD64",
    "python_version": "3.14.5",
}


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Create a separate SQLite database for each test.
    test_database = tmp_path / "test_patchops.db"

    # Redirect database connections to the temporary database.
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database,
    )

    # Initialize the temporary database.
    database.initialize_database()

    # The database path is restored after each test.
    with TestClient(app) as test_client:
        yield test_client


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "PatchOps",
        "message": "PatchOps API is running",
    }


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "patchops-api",
    }


def test_register_device(client):
    response = client.post(
        "/devices/register",
        json=TEST_DEVICE,
    )

    assert response.status_code == 201
    assert response.json()["device"] == TEST_DEVICE


def test_list_devices(client):
    client.post(
        "/devices/register",
        json=TEST_DEVICE,
    )

    response = client.get("/devices")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["hostname"] == "PATCHOPS-TEST"


def test_get_device(client):
    client.post(
        "/devices/register",
        json=TEST_DEVICE,
    )

    response = client.get("/devices/test-device-001")

    assert response.status_code == 200
    assert response.json()["device_id"] == "test-device-001"


def test_device_not_found(client):
    response = client.get("/devices/nonexistent")

    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_duplicate_registration(client):
    client.post(
        "/devices/register",
        json=TEST_DEVICE,
    )

    updated_device = {
        **TEST_DEVICE,
        "hostname": "PATCHOPS-UPDATED",
    }

    response = client.post(
        "/devices/register",
        json=updated_device,
    )

    assert response.status_code == 201

    devices_response = client.get("/devices")
    devices = devices_response.json()

    assert len(devices) == 1
    assert devices[0]["hostname"] == "PATCHOPS-UPDATED"
