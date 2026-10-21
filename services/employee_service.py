from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import employee_repository


async def create_employee(db: AsyncSession, data):
    return await employee_repository.create_employee(db, data)


async def assign_projects(
    db: AsyncSession,
    employee_id: int,
    project_ids: list[int],
):
    employee = await employee_repository.assign_projects(
        db, employee_id, project_ids
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee or one or more projects not found",
        )

    return employee


async def get_employee(db: AsyncSession, employee_id: int):
    employee = await employee_repository.get_employee_eager(
        db, employee_id
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


async def get_employees(db: AsyncSession, page: int, page_size: int):
    return await employee_repository.get_employees_paginated(
        db, page, page_size
    )