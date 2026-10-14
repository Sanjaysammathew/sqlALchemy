from sqlalchemy import select
from sqlalchemy.orm import Session

from models.employee import Employee
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate


def get_all(db: Session) -> list[Employee]:
    return db.scalars(select(Employee)).all()


def get_by_id(db: Session, employee_id: int) -> Employee | None:
    return db.get(Employee, employee_id)


def create(db: Session, employee_data: EmployeeCreate) -> Employee:
    employee = Employee(**employee_data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    for field, value in employee_data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


def delete(db: Session, employee_id: int) -> bool:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return False

    db.delete(employee)
    db.commit()
    return True
