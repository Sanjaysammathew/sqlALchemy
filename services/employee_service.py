from sqlalchemy.orm import Session

from repositories import employee_repository
from models.employee import Employee
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate


def get_all_employees(db: Session) -> list[Employee]:
    return employee_repository.get_all(db)


def get_employee_by_id(db: Session, employee_id: int) -> Employee | None:
    return employee_repository.get_by_id(db, employee_id)


def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    return employee_repository.create(db, employee_data)


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee | None:
    return employee_repository.update(db, employee_id, employee_data)


def delete_employee(db: Session, employee_id: int) -> bool:
    return employee_repository.delete(db, employee_id)
