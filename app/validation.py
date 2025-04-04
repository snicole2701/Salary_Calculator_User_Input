valid_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def validate_month(data):
    if "month" not in data or data["month"] not in valid_months:
        return "Month must be a valid month name (e.g., 'January')."
    return None

def validate_year(data):
    if "year" not in data or not (1900 <= data["year"] <= 2100):
        return "Year must be an integer between 1900 and 2100."
    return None

def validate_age(data):
    if "age" not in data or not (0 <= data["age"] <= 120):
        return "Age must be an integer between 0 and 120."
    return None

def validate_income_fields(data):
    income_fields = ["basic_salary", "commission", "bonus", "overtime", "leave_pay"]
    errors = []
    for field in income_fields:
        if field in data:
            if not isinstance(data[field], (int, float)) or data[field] < 0:
                errors.append(f"{field} must be a positive number if provided.")
    return errors

def validate_input(data):
    errors = []

    month_error = validate_month(data)
    if month_error:
        errors.append(month_error)

    year_error = validate_year(data)
    if year_error:
        errors.append(year_error)

    age_error = validate_age(data)
    if age_error:
        errors.append(age_error)

    income_errors = validate_income_fields(data)
    errors.extend(income_errors)

    if errors:
        return {"is_valid": False, "errors": errors}
    return {"is_valid": True, "errors": []}