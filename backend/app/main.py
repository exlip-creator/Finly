from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}