
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "PatchOps",
        "message": "PatchOps API is running"
    }


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "patchops-api"
    }

from fastapi.testclient import TestClient
from backend.app.main import app, devices

client = TestClient(app)

TEST_DEVICE = {
    "device_id": "test-device-001",
    "hostname": "PATCHOPS-TEST",
    "operating_system": "Windows",
    "os_version": "10.0.26200",
    "os_release": "11",
    "architecture": "AMD64",
    "python_version": "3.14.5"
}


def test_register_device():
    devices.clear()

    response = client.post(
        "/devices/register",
        json=TEST_DEVICE
    )

    assert response.status_code == 201
    assert response.json()["device"] == TEST_DEVICE


def test_list_devices():
    devices.clear()

    client.post("/devices/register", json=TEST_DEVICE)

    response = client.get("/devices")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["hostname"] == "PATCHOPS-TEST"


def test_get_device():
    devices.clear()

    client.post("/devices/register", json=TEST_DEVICE)

    response = client.get("/devices/test-device-001")

    assert response.status_code == 200
    assert response.json()["device_id"] == "test-device-001"


def test_device_not_found():
    devices.clear()

    response = client.get("/devices/nonexistent")

    assert response.status_code == 404


def test_duplicate_registration():
    devices.clear()

    client.post("/devices/register", json=TEST_DEVICE)

    response = client.post(
        "/devices/register",
        json=TEST_DEVICE
    )

    assert response.status_code == 201
    assert len(devices) == 1
