from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.employee_schema import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from services import employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    return employee_service.create_employee(db, employee_data)


@router.get("/", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)) -> list[EmployeeResponse]:
    return employee_service.get_all_employees(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    employee = employee_service.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    employee = employee_service.update_employee(db, employee_id, employee_data)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    if not employee_service.delete_employee(db, employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return {"message": "Employee deleted successfully"}
