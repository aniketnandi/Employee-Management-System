from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_writer
from app.db.session import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentRead

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[DepartmentRead])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).order_by(Department.name).all()


@router.post(
    "/",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_writer)],
)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    name = data.name.strip()
    if db.query(Department).filter(Department.name == name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department already exists")
    department = Department(name=name)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_writer)],
)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    # Detach employees explicitly so behaviour is the same on every database backend.
    for employee in department.employees:
        employee.department_id = None
    db.delete(department)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
