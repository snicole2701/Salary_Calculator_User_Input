import requests
import logging
from flask import Flask, request, jsonify
import os
from app import create_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URLs for services
CALCULATIONS_SERVICE_URL = os.getenv("CALCULATIONS_SERVICE_URL", "https://salary-calculator-calculation-service.onrender.com")

# Global variable to store user input
user_input_data = None

# Create the Flask app
app = create_app()

@app.route('/')
def home():
    """Home route."""
    logger.info("Accessing home route.")
    return "Welcome to the Salary Calculator Service!"

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    logger.info("Health endpoint accessed.")
    return jsonify({"status": "OK"}), 200

@app.route('/add-user-input', methods=['POST'])
def add_user_input():
    """
    Endpoint to add user input and store it for retrieval.
    """
    global user_input_data
    logger.info("Received request at /add-user-input")
    user_input = request.json

    # Validate input data
    if not user_input:
        logger.warning("Invalid user input received.")
        return jsonify({"error": "Invalid user input"}), 400

    # Store the user input globally
    user_input_data = user_input
    logger.info(f"User input stored: {user_input}")
    return jsonify({"message": "User input stored successfully!"}), 200

@app.route('/get-user-input', methods=['GET'])
def get_user_input():
    """
    Endpoint to retrieve stored user input for other services.
    """
    global user_input_data
    if not user_input_data:
        logger.warning("No user input found.")
        return jsonify({"error": "No user input available."}), 404

    logger.info(f"Serving user input: {user_input_data}")
    return jsonify(user_input_data), 200

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    """Endpoint to send feedback to the Feedback Service."""
    logger.info("Received request at /send-feedback")
    feedback_data = request.json
    if not feedback_data:
        logger.warning("Invalid feedback data received.")
        return jsonify({"error": "Invalid feedback data"}), 400

    url = os.getenv("FEEDBACK_SERVICE_BASE_URL", "http://placeholder-feedback-service-url.com") + "/send-feedback"
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

@app.route('/test-calculations-service')
def test_calculations_service():
    """Endpoint to test connection with Calculations Service."""
    logger.info("Testing connection with Calculations Service...")
    url = f"{CALCULATIONS_SERVICE_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Calculations Service is healthy.")
            return jsonify({"calculations_service_status": "Healthy"}), 200
        else:
            logger.warning("Calculations Service is unhealthy.")
            return jsonify({"calculations_service_status": "Unhealthy"}), 500
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Calculations Service: {e}")
        return jsonify({"error": f"Failed to connect: {e}"}), 500

if __name__ == '__main__':
    logger.info("Starting Salary Calculator Service...")
    try:
        debug_mode = os.getenv("DEBUG", "False").lower() == "true"
        port = int(os.getenv("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
    except Exception as e:
        logger.error(f"Error starting the service: {e}")