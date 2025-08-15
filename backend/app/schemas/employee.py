from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: Optional[str] = None
    join_date: Optional[date] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    join_date: Optional[date] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None

class EmployeeRead(EmployeeBase):
    id: int
    class Config:
        from_attributes = True