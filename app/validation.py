valid_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def validate_month(data):
    print("Validating month...")
    if "month" not in data or data["month"] not in valid_months:
        print("Invalid month:", data.get("month", None))
        return "Month must be a valid month name (e.g., 'January')."
    return None

def validate_year(data):
    print("Validating year...")
    if "year" not in data or not (1900 <= data["year"] <= 2100):
        print("Invalid year:", data.get("year", None))
        return "Year must be an integer between 1900 and 2100."
    return None

def validate_age(data):
    print("Validating age...")
    if "age" not in data or not (0 <= data["age"] <= 120):
        print("Invalid age:", data.get("age", None))
        return "Age must be an integer between 0 and 120."
    return None

def validate_income_fields(data):
    print("Validating income fields...")
    income_fields = ["basic_salary", "commission", "bonus", "overtime", "leave_pay"]
    errors = []
    for field in income_fields:
        if field in data:
            print(f"Checking {field}: {data[field]}")
            if not isinstance(data[field], (int, float)) or data[field] < 0:
                print(f"Invalid {field}: {data[field]}")
                errors.append(f"{field} must be a positive number if provided.")
    return errors

def validate_input(data):
    print("Starting validation...")
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
        print("Validation failed with errors:", errors)
        return {"is_valid": False, "errors": errors}
    
    print("Validation successful!")
    return {"is_valid": True, "errors": []}