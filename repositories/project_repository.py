from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.projects import Projects


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