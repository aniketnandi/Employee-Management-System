from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    role = Column(String(50), nullable=True)
    join_date = Column(Date, nullable=True)
    salary = Column(Float, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    # optional: define relationship if needed
    # department = relationship("Department", backref="employees")