
from fastapi import FastAPI

app = FastAPI(
    title="PatchOps API",
    description="Automated patch management platform",
    version="0.1.0"
)


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