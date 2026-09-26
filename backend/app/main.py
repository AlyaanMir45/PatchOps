
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="PatchOps API",
    description="Automated patch management platform",
    version="0.1.0"
)


# Device data model
class Device(BaseModel):
    device_id: str
    hostname: str
    operating_system: str
    os_version: str
    os_release: str
    architecture: str
    python_version: str


# Temporary in-memory device registry
devices: dict[str, Device] = {}


# Existing endpoints
@app.get("/")
def root():
    return {
        "application": "PatchOps",
        "message": "PatchOps API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "patchops-api"
    }


# New device registration endpoint
@app.post("/devices/register", status_code=201)
def register_device(device: Device):
    devices[device.device_id] = device

    return {
        "message": "Device registered successfully",
        "device": device
    }


# Retrieve all registered devices
@app.get("/devices")
def list_devices():
    return list(devices.values())


# Retrieve a specific device
@app.get("/devices/{device_id}")
def get_device(device_id: str):
    from fastapi import HTTPException

    if device_id not in devices:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return devices[device_id]
