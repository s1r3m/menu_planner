from flask import Flask, request, jsonify, send_from_directory
from flask.typing import Response

app = Flask(__name__, static_folder='../frontend')

# Define mock user data
users_data = {
    'santa_clause': [
        {'name': 'Week 1'},
        {'name': 'Xmas Week'},
    ],
    'Filipp': [],  # No weeks added for Filipp
}


@app.route('/ping')
def ping() -> Response:
    return jsonify('pong')


@app.route('/')
def home() -> Response:
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:filename>')
def static_files(filename) -> Response:
    """Serve static files like CSS, images, and additional HTML pages."""
    return send_from_directory(app.static_folder, filename)


@app.route('/get-weeks', methods=['POST'])
def get_weeks() -> Response:
    """Endpoint to retrieve weeks data based on the button clicked."""
    # Parse the request parameter
    button_name = request.json.get('button')

    # Determine response based on the button pressed
    match button_name:
        case 'login':
            response = {
                'username': 'Santa Clause',
                'weeks': users_data['santa_clause'],
            }
        case 'signup':
            response = {
                'username': 'Filipp',
                'weeks': users_data['Filipp'],
            }
        case _:
            response = {
                'username': 'Unkown User',
                'weeks': [],
            }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
