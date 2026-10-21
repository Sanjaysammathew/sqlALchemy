from fastapi import HTTPException

from ports.repository_ports import EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    async def create_employee(self, data):
        return await self.repository.create_employee(data)

    async def assign_projects(self, employee_id: int, project_ids: list[int]):
        employee = await self.repository.assign_projects(employee_id, project_ids)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee or one or more projects not found",
            )

        return employee

    async def get_employee(self, employee_id: int):
        employee = await self.repository.get_employee_eager(employee_id)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )

        return employee

    async def get_employees(self, page: int, page_size: int):
        return await self.repository.get_employees_paginated(page, page_size)

    async def get_employees_with_join(self):
        return await self.repository.get_employees_with_join()

    async def get_employees_with_joinload(self):
        return await self.repository.get_employees_with_joinload()

    async def extend_project(self, employee_id: int, project_ids: list[int]):
        return await self.repository.extend_project(employee_id, project_ids)