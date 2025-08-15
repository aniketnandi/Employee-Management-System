import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import auth as auth_routes
from app.api.v1 import employees as employee_routes
from app.api.v1 import departments as department_routes

# Create tables on startup (for dev). In prod, use Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EMS API", version="1.0.0")

# Allow your frontend dev server
origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(employee_routes.router, prefix="/api/v1/employees", tags=["employees"])
app.include_router(department_routes.router, prefix="/api/v1/departments", tags=["departments"])

@app.get("/")
def root():
    return {"message": "Employee Management API is running 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)