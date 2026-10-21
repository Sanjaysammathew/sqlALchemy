from sqlalchemy import Column, ForeignKey, Integer, Table

from config.database import Base


employee_project = Table(
    "employee_project",
    Base.metadata,
    Column(
        "employee_id",
        Integer,
        ForeignKey("Employee.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "project_id",
        Integer,
        ForeignKey("Projects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)