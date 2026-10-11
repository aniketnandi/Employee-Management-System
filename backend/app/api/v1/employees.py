from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_writer
from app.db.session import get_db
from app.models.department import Department
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate

router = APIRouter(dependencies=[Depends(get_current_user)])


def _get_or_404(db: Session, employee_id: int) -> Employee:
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


def _validate_references(db: Session, *, email: str | None, department_id: int | None, exclude_id: int | None = None):
    if email is not None:
        query = db.query(Employee).filter(Employee.email == email)
        if exclude_id is not None:
            query = query.filter(Employee.id != exclude_id)
        if query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    if department_id is not None and not db.get(Department, department_id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Department does not exist")


@router.get("/", response_model=list[EmployeeRead])
def list_employees(
    q: str | None = Query(default=None, description="Case-insensitive search on name, email or role"),
    department_id: int | None = Query(default=None, description="Only employees in this department"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)
    if q:
        pattern = f"%{q.strip()}%"
        query = query.filter(
            or_(Employee.name.ilike(pattern), Employee.email.ilike(pattern), Employee.role.ilike(pattern))
        )
    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)
    return query.order_by(Employee.name).offset(skip).limit(limit).all()


@router.post(
    "/",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_writer)],
)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    _validate_references(db, email=data.email, department_id=data.department_id)
    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, employee_id)


@router.put("/{employee_id}", response_model=EmployeeRead, dependencies=[Depends(require_writer)])
def update_employee(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = _get_or_404(db, employee_id)
    changes = data.model_dump(exclude_unset=True)
    _validate_references(
        db, email=changes.get("email"), department_id=changes.get("department_id"), exclude_id=employee_id
    )
    for field, value in changes.items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_writer)],
)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db.delete(_get_or_404(db, employee_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
