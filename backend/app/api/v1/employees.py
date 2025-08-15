from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[EmployeeRead])
def list_employees(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Employee).all()

@router.post("/", response_model=EmployeeRead)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    emp = Employee(**data.model_dump())
    db.add(emp); db.commit(); db.refresh(emp)
    return emp

@router.get("/{emp_id}", response_model=EmployeeRead)
def get_employee(emp_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    emp = db.get(Employee, emp_id)
    if not emp: raise HTTPException(status_code=404, detail="Not found")
    return emp

@router.put("/{emp_id}", response_model=EmployeeRead)
def update_employee(emp_id: int, data: EmployeeUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    emp = db.get(Employee, emp_id)
    if not emp: raise HTTPException(status_code=404, detail="Not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(emp, k, v)
    db.add(emp); db.commit(); db.refresh(emp)
    return emp

@router.delete("/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    emp = db.get(Employee, emp_id)
    if not emp: raise HTTPException(status_code=404, detail="Not found")
    db.delete(emp); db.commit()
    return {"status": "deleted"}