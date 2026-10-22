from abc import ABC, abstractmethod
from typing import Any


class EmployeeInterface(ABC):
    @abstractmethod
    async def create_employee(self, data: Any) -> Any:
        pass

    @abstractmethod
    async def assign_projects(
        self, employee_id: int, project_ids: list[int]
    ) -> Any:
        pass

    @abstractmethod
    async def get_employee_eager(self, employee_id: int) -> Any:
        pass

    @abstractmethod
    async def get_employees_paginated(
        self, page: int, page_size: int
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def get_employees_with_join(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def get_employees_with_joinload(self) -> list[Any]:
        pass

    @abstractmethod
    async def extend_project(
        self, employee_id: int, project_ids: list[int]
    ) -> Any:
        pass


class ProjectInterface(ABC):
    @abstractmethod
    async def create_project(self, data: Any) -> Any:
        pass

    @abstractmethod
    async def get_all_projects(self) -> list[Any]:
        pass
