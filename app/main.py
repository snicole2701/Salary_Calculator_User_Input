from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)