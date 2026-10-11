# Import all models so they are registered on Base.metadata (used by Alembic and tests).
from app.models.department import Department
from app.models.employee import Employee
from app.models.user import User

__all__ = ["Department", "Employee", "User"]
