from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.api.routes import router
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is migration-only. Run Alembic upgrade before starting the API.
    yield
    await engine.dispose()
app=FastAPI(title=settings.app_name,version="0.2.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,allow_methods=["GET","POST"],allow_headers=["Authorization","Content-Type"])
app.include_router(router,prefix="/api/v1")
