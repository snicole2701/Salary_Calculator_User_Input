import requests
import logging
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import os
from app import create_app
from app.validation import validate_input

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URLs for services
TAX_SERVICE_BASE_URL = os.getenv("TAX_SERVICE_BASE_URL", "https://salary-calculator-tax-tables-service.onrender.com")
USER_INPUT_SERVICE_URL = os.getenv("USER_INPUT_SERVICE_URL", "https://salary-calculator-user-input.onrender.com")
CALCULATIONS_SERVICE_URL = os.getenv("CALCULATIONS_SERVICE_URL", "https://salary-calculator-calculation-service.onrender.com")
FEEDBACK_SERVICE_BASE_URL = os.getenv("FEEDBACK_SERVICE_BASE_URL", "http://placeholder-feedback-service-url.com")  # Placeholder for Feedback Service URL
REBATE_DB_URI = os.getenv("REBATE_DB_URI")
TAX_DB_URI = os.getenv("TAX_DB_URI")

# Create the Flask app
app = create_app()

@app.route('/')
def home():
    """Home route."""
    logger.info("Accessing home route.")
    return "Welcome to the Salary Calculator Service!"

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
        logger.info(f"Validation successful. Age group assigned: {result['data'].get('age_group')}")
        return jsonify(result), 200
    return jsonify(result), 400

@app.route('/fetch-tax-details', methods=['POST'])
def fetch_tax_details():
    """Endpoint to query the Tax Tables Service."""
    logger.info("Received request at /fetch-tax-details")
    data = request.json
    if not data:
        logger.warning("Invalid JSON received.")
        return jsonify({"error": "Invalid request"}), 400

    validation_result = validate_input(data)
    if not validation_result["is_valid"]:
        logger.warning(f"Validation failed: {validation_result['errors']}")
        return jsonify(validation_result), 400

    validated_data = validation_result["data"]
    payload = {
        "month": validated_data.get("month"),
        "year": validated_data.get("year"),
        "income": validated_data.get("basic_salary"),  # Example income field
        "age_group": validated_data.get("age_group")
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

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    """Endpoint to send feedback to the Feedback Service."""
    logger.info("Received request at /send-feedback")
    feedback_data = request.json
    if not feedback_data:
        logger.warning("Invalid feedback data received.")
        return jsonify({"error": "Invalid feedback data"}), 400

    url = f"{FEEDBACK_SERVICE_BASE_URL}/send-feedback"
    try:
        response = requests.post(url, json=feedback_data)
        if response.status_code == 200:
            logger.info("Feedback successfully sent.")
            return jsonify(response.json()), 200
        else:
            logger.error(f"Error sending feedback: {response.status_code}")
            return jsonify({"error": response.json().get("error", "Unknown error")}), 500
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Feedback Service: {e}")
        return jsonify({"error": "Connection to Feedback Service failed"}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to send data to Calculations Service."""
    logger.info("Received request at /calculate")
    calculation_data = request.json
    if not calculation_data:
        logger.warning("Invalid calculation data received.")
        return jsonify({"error": "Invalid calculation data"}), 400

    url = f"{CALCULATIONS_SERVICE_URL}/perform-calculations"
    try:
        response = requests.post(url, json=calculation_data)
        if response.status_code == 200:
            logger.info("Calculations successfully performed.")
            return jsonify(response.json()), 200
        else:
            logger.error(f"Error performing calculations: {response.status_code}")
            return jsonify({"error": response.json().get("error", "Unknown error")}), 500
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Calculations Service: {e}")
        return jsonify({"error": "Connection to Calculations Service failed"}), 500

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