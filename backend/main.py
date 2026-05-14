import uvicorn
from fastapi import FastAPI,APIRouter
from .app.routers.user import router as auth_router

app = FastAPI()

app.include_router(auth_router, tags=["auth"])




if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")