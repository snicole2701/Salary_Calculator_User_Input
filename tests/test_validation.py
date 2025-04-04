import pytest
from app.validation import validate_input

def test_validate_input():
    valid_data = {
        "month": "April",
        "year": 2025,
        "age": 30,
        "basic_salary": 50000,
        "bonus": 10000
    }
    assert validate_input(valid_data) == {"is_valid": True, "errors": []}

    invalid_data = {
        "month": "Aprril",  # Invalid month
        "year": 1800,  # Invalid year
        "age": -5,  # Invalid age
        "basic_salary": -50000,  # Invalid value
        "bonus": "invalid"  # Invalid type
    }
    result = validate_input(invalid_data)
    assert result["is_valid"] is False
    assert len(result["errors"]) > 0