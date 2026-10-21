from pydantic import BaseModel, ConfigDict
from schemas.project_schema import ProjectSummary


class EmployeeCreate(BaseModel):
    name: str
    salary: float


class EmployeeCreated(BaseModel):
    id: int
    name: str
    salary: float


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    salary: float
    projects: list[ProjectSummary] = []


class AssignProjects(BaseModel):
    project_ids: list[int]