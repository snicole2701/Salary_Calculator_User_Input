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

@app.route('/trigger-calculations', methods=['POST'])
def trigger_calculations():
    """
    Endpoint to forward stored user input to the Calculations Service (Microservice 3).
    """
    global user_input_data
    if not user_input_data:
        logger.warning("No user input stored to send to Calculations Service.")
        return jsonify({"error": "No user input available to trigger calculations."}), 400

    url = f"{CALCULATIONS_SERVICE_URL}/perform-calculations"
    logger.info(f"Forwarding user input to Calculations Service at URL: {url}")

    try:
        response = requests.post(url, json=user_input_data)
        logger.info(f"Response from Calculations Service: {response.status_code} - {response.text}")

        if response.status_code == 200:
            logger.info("Calculations triggered successfully.")
            return jsonify(response.json()), 200
        else:
            logger.error(f"Error triggering calculations: {response.status_code} - {response.text}")
            return jsonify({"error": response.json().get("error", "Unknown error")}), 500
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Calculations Service: {e}")
        return jsonify({"error": "Connection to Calculations Service failed"}), 500

if __name__ == '__main__':
    logger.info("Starting Salary Calculator Service...")
    try:
        debug_mode = os.getenv("DEBUG", "False").lower() == "true"
        port = int(os.getenv("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
    except Exception as e:
        logger.error(f"Error starting the service: {e}")