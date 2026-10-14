import pytest
from pydantic import ValidationError
from schemas import EmployeeCreate, EmployeeUpdate


@pytest.fixture
def valid_employee_data() -> dict[str, object]:
    return {
        "name": "Alex Smith",
        "salary": 65000,
        "experience": 5,
    }


def test_employee_create_accepts_valid_data(
    valid_employee_data: dict[str, object],
) -> None:
    employee = EmployeeCreate(**valid_employee_data)

    assert employee.name == "Alex Smith"
    assert employee.salary == 65000
    assert employee.experience == 5


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", ""),
        ("salary", 0),
        ("experience", -1),
    ],
)
def test_employee_create_rejects_invalid_data(
    valid_employee_data: dict[str, object],
    field: str,
    value: object,
) -> None:
    invalid_data = {**valid_employee_data, field: value}

    with pytest.raises(ValidationError):
        EmployeeCreate(**invalid_data)


def test_employee_update_accepts_partial_data() -> None:
    update = EmployeeUpdate(salary=70000)

    assert update.model_dump(exclude_unset=True) == {"salary": 70000}
