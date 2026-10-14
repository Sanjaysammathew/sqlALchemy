from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from models import Employee
from routers.employee_router import router
from config.database import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    Employee.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Employee Management API", lifespan=lifespan)
app.include_router(router)


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Employee API is running"}
