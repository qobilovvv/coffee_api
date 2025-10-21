from fastapi import FastAPI

from app.api.v1.admins_router import admins_router
from app.api.v1.auth_views import auth_router
from app.core.config import settings

app = FastAPI(title="Coffee API")

# @app.on_event("startup")
# async def on_startup():
#     await init_models()

app.include_router(router=auth_router, prefix="/auth", tags=["auth"])
app.include_router(router=admins_router)

@app.get("/")
async def root():
    return {"Hello": "Hello from Coffee API"}