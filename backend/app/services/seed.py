"""Optional demo data so the app is usable immediately after `docker compose up`."""

import logging
from datetime import date

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.department import Department
from app.models.employee import Employee
from app.models.user import User, UserRole
from app.services.auth import hash_password

logger = logging.getLogger(__name__)

DEPARTMENTS = ["Engineering", "Human Resources", "Finance", "Marketing"]

EMPLOYEES = [
    ("Priya Sharma", "priya.sharma@example.com", "Senior Software Engineer", "Engineering", 145000, date(2021, 3, 15)),
    ("Marcus Johnson", "marcus.johnson@example.com", "Engineering Manager", "Engineering", 170000, date(2019, 7, 1)),
    ("Elena Rossi", "elena.rossi@example.com", "HR Business Partner", "Human Resources", 98000, date(2022, 1, 10)),
    ("David Kim", "david.kim@example.com", "Financial Analyst", "Finance", 92000, date(2023, 5, 22)),
    ("Aisha Bello", "aisha.bello@example.com", "Product Marketing Lead", "Marketing", 118000, date(2020, 11, 2)),
    ("Tom Nguyen", "tom.nguyen@example.com", "Software Engineer", "Engineering", 120000, date(2024, 2, 5)),
]


def seed_demo_data(db: Session) -> None:
    if not db.query(User).filter(User.username == settings.demo_admin_username).first():
        db.add(
            User(
                username=settings.demo_admin_username,
                email=f"{settings.demo_admin_username}@example.com",
                hashed_password=hash_password(settings.demo_admin_password),
                role=UserRole.ADMIN,
            )
        )
        logger.info("Created demo admin user '%s'", settings.demo_admin_username)

    if db.query(Department).count() == 0 and db.query(Employee).count() == 0:
        departments = {name: Department(name=name) for name in DEPARTMENTS}
        db.add_all(departments.values())
        db.add_all(
            Employee(name=n, email=e, role=r, department=departments[d], salary=s, join_date=j)
            for n, e, r, d, s, j in EMPLOYEES
        )
        logger.info("Seeded %d departments and %d employees", len(DEPARTMENTS), len(EMPLOYEES))

    db.commit()
