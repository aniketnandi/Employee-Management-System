from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, departments, employees
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.seed import seed_demo_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    # The schema is managed by Alembic (`alembic upgrade head`); seeding only inserts rows.
    if settings.seed_demo_data:
        with SessionLocal() as db:
            seed_demo_data(db)
    yield


app = FastAPI(
    title="Employee Management System API",
    version="1.0.0",
    description="REST API for managing employees and departments, secured with JWT authentication.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(employees.router, prefix="/api/v1/employees", tags=["employees"])
app.include_router(departments.router, prefix="/api/v1/departments", tags=["departments"])


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
