from sqlalchemy.ext.asyncio import AsyncSession

from repositories import employee_repository
from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate
from pathlib import Path
from fastapi import HTTPException, UploadFile
from services.file_service import save_resume


async def get_all_employees(
    db: AsyncSession, page: int, page_size: int
) -> list[Employee]:
    return await employee_repository.get_all(db, page, page_size)


async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Employee | None:
    return await employee_repository.get_by_id(db, employee_id)


async def create_employee(db: AsyncSession, employee_data: EmployeeCreate) -> Employee:
    return await employee_repository.create(db, employee_data)


async def update_employee(
    db: AsyncSession,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee | None:
    return await employee_repository.update(db, employee_id, employee_data)


async def delete_employee(db: AsyncSession, employee_id: int) -> bool:
    return await employee_repository.delete(db, employee_id)


async def upload_employee_resume(
    db: AsyncSession,
    employee_id: int,
    file: UploadFile,
) -> dict:
    # Step 1: Check whether the employee exists
    employee = await employee_repository.get_by_id(db, employee_id)

    if employee is None:
        await file.close()
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    old_resume_path = employee.resume_path

    # Step 2: Validate the PDF
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        await file.close()
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    if file.content_type != "application/pdf":
        await file.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type",
        )

    # Step 3: Save the file in chunks
    file_path = await save_resume(file)

    # Step 4: Save the path in PostgreSQL
    try:
        updated = await employee_repository.save_resume_path(
            db,
            employee_id,
            file_path,
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )

        # Clean up previous resume file if one exists
        if old_resume_path and old_resume_path != file_path:
            Path(old_resume_path).unlink(missing_ok=True)

    except Exception:
        # Remove the file if its database update fails
        Path(file_path).unlink(missing_ok=True)
        raise

    # Step 5: Return the response
    return {
        "message": "Resume uploaded successfully",
        "employee_id": employee_id,
        "file_path": file_path,
    }
