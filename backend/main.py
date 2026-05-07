from fastapi import FastAPI,APIRouter
from .app.routers.auth import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/auth",tags=["auth"])