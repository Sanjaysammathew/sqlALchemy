from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from schemas.employee_schema import (
    EmployeeCreate,
    EmployeeCreated,
    EmployeeResponse,
    AssignProjects,
)
from services import employee_service
from repositories import employee_repository

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeCreated)
async def create_employee(
    data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
):
    return await employee_service.create_employee(db, data)


@router.put("/{employee_id}/projects", response_model=EmployeeResponse)
async def assign_projects(
    employee_id: int,
    data: AssignProjects,
    db: AsyncSession = Depends(get_db),
):
    return await employee_service.assign_projects(db, employee_id, data.project_ids)


@router.get("/", response_model=dict)
async def get_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await employee_service.get_employees(db, page, page_size)

    return {
        **result,
        "items": [
            EmployeeResponse.model_validate(employee) for employee in result["items"]
        ],
    }


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await employee_service.get_employee(db, employee_id)


@router.get("/reports/employees-projects")
async def employees_projects_report(db: AsyncSession = Depends(get_db)):
    return await employee_repository.get_employees_with_join(db)


@router.get("/queries/join-load", response_model=list[EmployeeResponse])
async def join_load(db: AsyncSession = Depends(get_db)):
    employees = await employee_repository.get_employees_with_joinload(db)
    return employees


@router.patch("/{employee_id}")
async def extend_project(
    employee_id: int, data: AssignProjects, db: AsyncSession = Depends(get_db)
):
    return await employee_repository.extend_project(
        db, employee_id, data.project_ids
    )
