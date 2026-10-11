from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    role: str | None = Field(default=None, max_length=50)
    join_date: date | None = None
    salary: float | None = Field(default=None, ge=0)
    department_id: int | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    role: str | None = Field(default=None, max_length=50)
    join_date: date | None = None
    salary: float | None = Field(default=None, ge=0)
    department_id: int | None = None


class EmployeeRead(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
