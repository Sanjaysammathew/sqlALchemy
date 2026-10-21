from sqlalchemy.ext.asyncio import AsyncSession

from repositories import project_repository


async def create_project(db: AsyncSession, data):
    return await project_repository.create_project(db, data)


async def get_projects(db: AsyncSession):
    return await project_repository.get_all_projects(db)