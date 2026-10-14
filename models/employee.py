from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("Name", String(100), nullable=False)
    experience: Mapped[int] = mapped_column("Experience", Integer, nullable=False)
    salary: Mapped[Decimal] = mapped_column("Salary", Numeric(10, 2), nullable=False)
