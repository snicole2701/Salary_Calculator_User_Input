from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import os
import logging
from app import create_app
from app.validation import validate_input
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URLs for services
TAX_SERVICE_BASE_URL = os.getenv("TAX_SERVICE_BASE_URL", "https://salary-calculator-tax-tables-service.onrender.com")
REBATE_DB_URI = os.getenv("REBATE_DB_URI")
TAX_DB_URI = os.getenv("TAX_DB_URI")

# Create the Flask app
app = create_app()

# Default route for the root URL
@app.route('/')
def home():
    logger.info("Accessing home route.")
    return "Welcome to the Salary Calculator Service!"

# Endpoint to validate user input
@app.route('/validate', methods=['POST'])
def validate():
    """Endpoint to validate user input."""
    logger.info("Received request at /validate")

    data = request.json
    if not data:
        logger.warning("Invalid JSON received.")
        return jsonify({"error": "Invalid request"}), 400

    logger.info(f"Data received: {data}")
    result = validate_input(data)
    logger.info(f"Validation result: {result}")

    if result["is_valid"]:
        # Include the updated data (e.g., total_income and total_income_excluding_commission) in the response
        return jsonify(result), 200
    return jsonify(result), 400

# Endpoint to query the Tax Tables Service
@app.route('/fetch-tax-details', methods=['POST'])
def fetch_tax_details():
    """Endpoint to query the Tax Tables Service."""
    logger.info("Received request at /fetch-tax-details")

    data = request.json
    if not data:
        logger.warning("Invalid JSON received.")
        return jsonify({"error": "Invalid request"}), 400

    # Validate user input before querying the Tax Service
    validation_result = validate_input(data)
    if not validation_result["is_valid"]:
        logger.warning(f"Validation failed: {validation_result['errors']}")
        return jsonify(validation_result), 400

    # Extract validated data
    validated_data = validation_result["data"]
    total_income = validated_data.get("total_income")
    total_income_excluding_commission = validated_data.get("total_income_excluding_commission")

    logger.info(f"Total Income: {total_income}, Total Income Excluding Commission: {total_income_excluding_commission}")

    # Pass data to Tax Tables Service
    payload = {
        "month": validated_data.get("month"),
        "year": validated_data.get("year"),
        "income": total_income
    }
    url = f"{TAX_SERVICE_BASE_URL}/get-tax-details"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            tax_details = response.json()
            logger.info(f"Tax details retrieved successfully: {tax_details}")
            return jsonify({"tax_details": tax_details}), 200
        else:
            logger.error(f"Error from Tax Tables Service: {response.json().get('error', 'Unknown error')}")
            return jsonify({"error": response.json().get("error", "Unknown error")}), 500
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Tax Tables Service: {e}")
        return jsonify({"error": "Connection to Tax Tables Service failed"}), 500

# Endpoint to test database connections
@app.route('/test-db')
def test_db_connection():
    """Endpoint to test database connections."""
    logger.info("Received request at /test-db.")

    if not REBATE_DB_URI or not TAX_DB_URI:
        logger.error("Database URIs not configured.")
        return jsonify({"error": "Database URIs not configured"}), 500

    rebate_engine = create_engine(REBATE_DB_URI)
    tax_engine = create_engine(TAX_DB_URI)

    try:
        with rebate_engine.connect() as conn:
            rebate_test = "Rebate DB Connected"
        with tax_engine.connect() as conn:
            tax_test = "Tax DB Connected"
        logger.info("Database connections successful.")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"rebate_db_status": rebate_test, "tax_db_status": tax_test}), 200

# Endpoint to test connection with the Tax Tables Service
@app.route('/test-tax-service')
def test_tax_service():
    """Endpoint to test connection with Tax Tables Service."""
    logger.info("Testing connection with Tax Tables Service...")
    url = f"{TAX_SERVICE_BASE_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Tax Tables Service is healthy.")
            return jsonify({"tax_service_status": "Healthy"}), 200
        else:
            logger.warning("Tax Tables Service is unhealthy.")
            return jsonify({"tax_service_status": "Unhealthy"}), 500
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Tax Tables Service: {e}")
        return jsonify({"error": f"Failed to connect: {e}"}), 500

if __name__ == '__main__':
    logger.info("Starting Salary Calculator Service...")
    try:
        debug_mode = os.getenv("DEBUG", "False").lower() == "true"
        port = int(os.getenv("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
    except Exception as e:
        logger.error(f"Error starting the service: {e}")