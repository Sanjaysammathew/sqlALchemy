from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base
from models.association import employee_project

if TYPE_CHECKING:
    from models.employee import Employee


class Projects(Base):
    __tablename__ = "Projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        secondary=employee_project,
        back_populates="projects",
    )
    
