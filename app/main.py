from flask import request, jsonify
from app import create_app
from app.validation import validate_input

app = create_app()

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    result = validate_input(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)