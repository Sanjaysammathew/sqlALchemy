from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from schemas.project_schema import ProjectCreate, ProjectResponse
from services import project_service


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    return await project_service.create_project(db, data)


@router.get("/", response_model=list[ProjectResponse])
async def get_projects(db: AsyncSession = Depends(get_db)):
    return await project_service.get_projects(db)