from ports.repository_ports import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(self, data):
        return await self.repository.create_project(data)

    async def get_projects(self):
        return await self.repository.get_all_projects()