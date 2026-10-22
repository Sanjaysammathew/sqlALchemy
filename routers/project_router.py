from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from interface.repository_ports import ProjectInterface
from repositories.project_repository import SqlAlchemyProjectRepository
from schemas.project_schema import ProjectCreate, ProjectResponse
from services.project_service import ProjectService


router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_repository(
    db: AsyncSession = Depends(get_db),
) -> ProjectInterface:
    return SqlAlchemyProjectRepository(db)


def get_project_service(
    repository: ProjectInterface = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(repository)


@router.post("/", response_model=ProjectResponse)
async def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    return await service.create_project(data)


@router.get("/", response_model=list[ProjectResponse])
async def get_projects(service: ProjectService = Depends(get_project_service)):
    return await service.get_projects()