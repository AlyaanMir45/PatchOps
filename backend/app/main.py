
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.database import (
    get_connection,
    initialize_database,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="PatchOps API",
    description="Automated patch management platform",
    version="0.1.0",
    lifespan=lifespan,
)


class Device(BaseModel):
    device_id: str
    hostname: str
    operating_system: str
    os_version: str
    os_release: str
    architecture: str
    python_version: str


@app.get("/")
def root():
    return {
        "application": "PatchOps",
        "message": "PatchOps API is running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "patchops-api",
    }


@app.post("/devices/register", status_code=201)
def register_device(device: Device):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO devices (
                device_id,
                hostname,
                operating_system,
                os_version,
                os_release,
                architecture,
                python_version
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                hostname = excluded.hostname,
                operating_system = excluded.operating_system,
                os_version = excluded.os_version,
                os_release = excluded.os_release,
                architecture = excluded.architecture,
                python_version = excluded.python_version
            """,
            (
                device.device_id,
                device.hostname,
                device.operating_system,
                device.os_version,
                device.os_release,
                device.architecture,
                device.python_version,
            ),
        )

    return {
        "message": "Device registered successfully",
        "device": device,
    }


@app.get("/devices")
def list_devices():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM devices ORDER BY hostname"
        ).fetchall()

    return [dict(row) for row in rows]


@app.get("/devices/{device_id}")
def get_device(device_id: str):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM devices WHERE device_id = ?",
            (device_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return dict(row)
