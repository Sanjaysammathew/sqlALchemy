from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    salary: float = Field(gt=0)
    experience: int = Field(ge=0)


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    salary: float | None = Field(default=None, gt=0)
    experience: int | None = Field(default=None, ge=0)


class EmployeeResponse(BaseModel):
    id: int
    name: str
    salary: float
    experience: int

    model_config = ConfigDict(from_attributes=True)
