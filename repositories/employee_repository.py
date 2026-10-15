from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate


async def get_all(db: AsyncSession) -> list[Employee]:
    return (await db.scalars(select(Employee))).all()


async def get_by_id(db: AsyncSession, employee_id: int) -> Employee | None:
    return await db.get(Employee, employee_id)


async def create(db: AsyncSession, employee_data: EmployeeCreate) -> Employee:
    employee = Employee(**employee_data.model_dump())
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return employee


async def update(
    db: AsyncSession,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee | None:
    employee = await db.get(Employee, employee_id)
    if employee is None:
        return None

    for field, value in employee_data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    await db.commit()
    await db.refresh(employee)
    return employee


async def delete(db: AsyncSession, employee_id: int) -> bool:
    employee = await db.get(Employee, employee_id)
    if employee is None:
        return False

    await db.delete(employee)
    await db.commit()
    return True


async def save_resume_path(
    db: AsyncSession,
    employee_id: int,
    file_path: str,
) -> bool:
    try:
        statement = (
            sa_update(Employee)
            .where(Employee.id == employee_id)
            .values(resume_path=file_path)
        )

        result = await db.execute(statement)

        if result.rowcount == 0:
            await db.rollback()
            return False

        await db.commit()
        return True

    except Exception:
        await db.rollback()
        raise
