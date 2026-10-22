from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.projects import Projects
from interface.repository_ports import ProjectInterface


async def create_project(db: AsyncSession, data):
    project = Projects(
        title=data.title,
        description=data.description,
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return project


async def get_all_projects(db: AsyncSession):
    statement = select(Projects).order_by(Projects.id)

    result = await db.scalars(statement)
    return result.all()


class SqlAlchemyProjectRepository(ProjectInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, data):
        return await create_project(self.db, data)

    async def get_all_projects(self):
        return await get_all_projects(self.db)