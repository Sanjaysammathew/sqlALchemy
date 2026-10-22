from fastapi import Depends

from config.database import get_db
from interface.repository_ports import EmployeeInterface, ProjectInterface
from repositories.employee_repository import SqlAlchemyEmployeeRepository
from repositories.project_repository import SqlAlchemyProjectRepository
from services.employee_service import EmployeeService
from sqlalchemy.ext.asyncio import AsyncSession

from services.project_service import ProjectService


def get_employee_repository(
    db: AsyncSession = Depends(get_db),
) -> EmployeeInterface:
    return SqlAlchemyEmployeeRepository(db)


def get_employee_service(
    repository: EmployeeInterface = Depends(get_employee_repository),
) -> EmployeeService:
    return EmployeeService(repository)


def get_project_repository(
    db: AsyncSession = Depends(get_db),
) -> ProjectInterface:
    return SqlAlchemyProjectRepository(db)


def get_project_service(
    repository: ProjectInterface = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(repository)
