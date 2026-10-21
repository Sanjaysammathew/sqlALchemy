from typing import TYPE_CHECKING

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base
from models.association import employee_project

if TYPE_CHECKING:
    from models.projects import Projects


class Employee(Base):
    __tablename__ = "Employee"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    salary: Mapped[int] = mapped_column(
        Numeric(10,2),
        nullable=False,
    )

    projects: Mapped[list["Projects"]] = relationship(
        "Projects",
        secondary=employee_project,
        back_populates="employees",
    )
