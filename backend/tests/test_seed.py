from app.models.department import Department
from app.models.employee import Employee
from app.models.user import User
from app.services.seed import seed_demo_data

from tests.conftest import TestingSessionLocal


def test_seed_is_idempotent():
    with TestingSessionLocal() as db:
        seed_demo_data(db)
        seed_demo_data(db)
        assert db.query(User).filter(User.role == "admin").count() == 1
        assert db.query(Department).count() == 4
        assert db.query(Employee).count() == 6
