from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query
from schemas.employee_schema import EmployeeProcedureInput
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from schemas.employee_schema import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from services import employee_service
from services.employee_service import upload_employee_resume

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    employee_data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
) -> EmployeeResponse:
    return await employee_service.create_employee(db, employee_data)


@router.get("/", response_model=list[EmployeeResponse])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> list[EmployeeResponse]:
    return await employee_service.get_all_employees(db, page, page_size)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
) -> EmployeeResponse:
    employee = await employee_service.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
) -> EmployeeResponse:
    employee = await employee_service.update_employee(db, employee_id, employee_data)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    if not await employee_service.delete_employee(db, employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return {"message": "Employee deleted successfully"}


@router.post("/{employee_id}/resume")
async def upload_resume(
    employee_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await upload_employee_resume(
        db,
        employee_id,
        file,
    )


@router.post("/procedure")
async def create_employee_procedure(
    employee: EmployeeProcedureInput,
    db: AsyncSession = Depends(get_db),
):
    return await employee_service.create_employee_using_procedure(db, employee)
