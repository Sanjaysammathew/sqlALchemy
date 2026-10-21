from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from ports.repository_ports import EmployeeRepository
from repositories.employee_repository import SqlAlchemyEmployeeRepository
from schemas.employee_schema import (
    EmployeeCreate,
    EmployeeCreated,
    EmployeeResponse,
    AssignProjects,
)
from services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_repository(
    db: AsyncSession = Depends(get_db),
) -> EmployeeRepository:
    return SqlAlchemyEmployeeRepository(db)


def get_employee_service(
    repository: EmployeeRepository = Depends(get_employee_repository),
) -> EmployeeService:
    return EmployeeService(repository)


@router.post("/", response_model=EmployeeCreated)
async def create_employee(
    data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    return await service.create_employee(data)


@router.put("/{employee_id}/projects", response_model=EmployeeResponse)
async def assign_projects(
    employee_id: int,
    data: AssignProjects,
    service: EmployeeService = Depends(get_employee_service),
):
    return await service.assign_projects(employee_id, data.project_ids)


@router.get("/", response_model=dict)
async def get_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: EmployeeService = Depends(get_employee_service),
):
    result = await service.get_employees(page, page_size)

    return {
        **result,
        "items": [
            EmployeeResponse.model_validate(employee) for employee in result["items"]
        ],
    }


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
):
    return await service.get_employee(employee_id)


@router.get("/reports/employees-projects")
async def employees_projects_report(
    service: EmployeeService = Depends(get_employee_service),
):
    return await service.get_employees_with_join()


@router.get("/queries/join-load", response_model=list[EmployeeResponse])
async def join_load(service: EmployeeService = Depends(get_employee_service)):
    employees = await service.get_employees_with_joinload()
    return employees


@router.patch("/{employee_id}")
async def extend_project(
    employee_id: int,
    data: AssignProjects,
    service: EmployeeService = Depends(get_employee_service),
):
    return await service.extend_project(employee_id, data.project_ids)
