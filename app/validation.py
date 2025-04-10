# Map of month names to numbers
month_to_number = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

def validate_month(data):
    """
    Validate the 'month' field to ensure it's valid.
    Args:
        data (dict): Input data.
    Returns:
        str or None: Error message if invalid, otherwise None.
    """
    print("Validating month...")
    if "month" not in data or data["month"] not in month_to_number:
        print("Invalid month:", data.get("month", None))
        return "Month must be a valid month name (e.g., 'January')."
    
    print("Month validated successfully.")
    return None

def convert_month_to_number(data):
    """
    Convert the validated month name to its corresponding number.
    Args:
        data (dict): Input data.
    Returns:
        None: Updates the input data directly with the month as an integer.
    """
    if "month" in data:
        data["month"] = month_to_number[data["month"]]
        print(f"Month converted to number: {data['month']}")

def validate_year(data):
    """
    Validate the 'year' field.
    Args:
        data (dict): Input data.
    Returns:
        str or None: Error message if invalid, otherwise None.
    """
    print("Validating year...")
    if "year" not in data or not isinstance(data["year"], int) or not (1900 <= data["year"] <= 2100):
        print("Invalid year:", data.get("year", None))
        return "Year must be an integer between 1900 and 2100."
    return None

def validate_age(data):
    """
    Validate the 'age' field and assign an age group based on the age.
    Args:
        data (dict): Input data.
    Returns:
        str or None: Error message if invalid, otherwise None.
    """
    print("Validating age...")
    if "age" not in data or not isinstance(data["age"], int) or not (0 <= data["age"] <= 120):
        print("Invalid age:", data.get("age", None))
        return "Age must be an integer between 0 and 120."

    # Assign age group
    age = data["age"]
    if age <= 64:
        data["age_group"] = "Primary"
    elif 65 <= age <= 74:
        data["age_group"] = "Secondary (65 and older)"
    else:
        data["age_group"] = "Tertiary (75 and older)"
    print(f"Age group assigned: {data['age_group']}")
    return None

def validate_income_fields(data):
    """
    Validate income-related fields such as 'basic_salary', 'commission', etc.
    Args:
        data (dict): Input data.
    Returns:
        list: List of error messages for invalid fields.
    """
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
    """
    Validate all fields in the input data.
    Args:
        data (dict): Input data.
    Returns:
        dict: Validation results with 'is_valid' flag and error messages.
    """
    print("Starting validation...")
    errors = []

    # Validate month first
    month_error = validate_month(data)
    if month_error:
        errors.append(month_error)
    else:
        # Convert month to number only if validation passed
        convert_month_to_number(data)

    # Proceed with other validations
    year_error = validate_year(data)
    if year_error:
        errors.append(year_error)

    age_error = validate_age(data)
    if age_error:
        errors.append(age_error)

    income_errors = validate_income_fields(data)
    errors.extend(income_errors)

    # Compile results
    if errors:
        print("Validation failed with errors:", errors)
        return {"is_valid": False, "errors": errors}

    print("Validation successful!")
    return {"is_valid": True, "data": data}