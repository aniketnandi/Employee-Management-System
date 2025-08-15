from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentRead
from app.api.v1.auth import get_current_user
router = APIRouter()

@router.get("/", response_model=List[DepartmentRead])
def list_departments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Department).all()

@router.post("/", response_model=DepartmentRead)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(Department).filter(Department.name == data.name).first():
        raise HTTPException(status_code=400, detail="Department exists")
    dep = Department(name=data.name)
    db.add(dep); db.commit(); db.refresh(dep)
    return dep