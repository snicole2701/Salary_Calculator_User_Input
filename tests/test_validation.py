import pytest
from app.validation import validate_input

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.validation import validate_input

def test_valid_data():
    data = {
        "month": "January",
        "year": 2025,
        "age": 30,
        "basic_salary": 5000,
        "commission": 200
    }
    result = validate_input(data)
    assert result["is_valid"] is True
    assert len(result["errors"]) == 0

def test_invalid_month():
    data = {"month": "NotAMonth", "year": 2025, "age": 30}
    result = validate_input(data)
    assert result["is_valid"] is False
    assert "Month must be a valid month name (e.g., 'January')." in result["errors"]

def test_invalid_year():
    data = {"month": "January", "year": 1800, "age": 30}
    result = validate_input(data)
    assert result["is_valid"] is False
    assert "Year must be an integer between 1900 and 2100." in result["errors"]

def test_invalid_age():
    data = {"month": "January", "year": 2025, "age": 150}
    result = validate_input(data)
    assert result["is_valid"] is False
    assert "Age must be an integer between 0 and 120." in result["errors"]

def test_negative_income():
    data = {
        "month": "January",
        "year": 2025,
        "age": 30,
        "basic_salary": -1000
    }
    result = validate_input(data)
    assert result["is_valid"] is False
    assert "basic_salary must be a positive number if provided." in result["errors"]