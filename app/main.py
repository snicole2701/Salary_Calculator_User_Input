from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import os
from app import create_app
from app.validation import validate_input

# Create the Flask app
app = create_app()

# Default route for the root URL
@app.route('/')
def home():
    return "Welcome to the Salary Calculator Service!"

# Endpoint to validate user input
@app.route('/validate', methods=['POST'])
def validate():
    """Endpoint to validate user input."""
    print("Received request at /validate")

    data = request.json
    if not data:
        print("Invalid JSON received")
        return jsonify({"error": "Invalid request"}), 400

    print(f"Data received: {data}")
    result = validate_input(data)
    print(f"Validation result: {result}")

    return jsonify(result), 200

# Endpoint to test database connections
@app.route('/test-db')
def test_db_connection():
    """Endpoint to test database connections."""
    rebate_db_uri = os.getenv("REBATE_DB_URI")
    tax_db_uri = os.getenv("TAX_DB_URI")
    rebate_engine = create_engine(rebate_db_uri)
    tax_engine = create_engine(tax_db_uri)

    try:
        with rebate_engine.connect() as conn:
            rebate_test = "Rebate DB Connected"
        with tax_engine.connect() as conn:
            tax_test = "Tax DB Connected"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"rebate_db_status": rebate_test, "tax_db_status": tax_test}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)