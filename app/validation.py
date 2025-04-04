def validate_input(data):
    errors = []
    valid_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Validate month
    if "month" not in data or data["month"] not in valid_months:
        errors.append("Month must be a valid month name (e.g., 'January').")

    # Validate year
    if "year" not in data or not (1900 <= data["year"] <= 2100):
        errors.append("Year must be an integer between 1900 and 2100.")

    # Validate age
    if "age" not in data or not (0 <= data["age"] <= 120):
        errors.append("Age must be an integer between 0 and 120.")

    # Validate income types (optional)
    income_fields = ["basic_salary", "commission", "bonus", "overtime", "leave_pay"]
    for field in income_fields:
        if field in data:
            if not isinstance(data[field], (int, float)) or data[field] < 0:
                errors.append(f"{field} must be a positive number if provided.")

    if errors:
        return {"is_valid": False, "errors": errors}
    return {"is_valid": True, "errors": []}