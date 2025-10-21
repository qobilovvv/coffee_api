from fastapi import FastAPI

from app.api.v1.auth_views import auth_router
from app.core.config import settings

app = FastAPI(title="Coffee API")

app.include_router(router=auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"Hello": "Hello from Coffee API"}