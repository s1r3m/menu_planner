from flask import Flask, request, jsonify

app = Flask(__name__)  # , static_url_path='/', static_folder='../frontend')

# Define mock user data
users_data = {
    'santa_clause': [
        {'name': 'Week 1'},
        {'name': 'Xmas Week'},
    ],
    'Filipp': [],  # No weeks added for Filipp
}

@app.route('/api/get_weeks', methods=['POST'])
def get_weeks():
    """Endpoint to retrieve weeks data based on the button clicked."""
    button_name = request.json.get('button')

    # Determine response based on the button pressed
    match button_name:
        case 'login':
            response = {
                'username': 'Santa Clause',
                'weeks': users_data['santa_clause'],
                'avatar': 'av1.png',
            }
        case 'signup':
            response = {
                'username': 'Filipp',
                'weeks': users_data['Filipp'],
                'avatar': 'av2.png',
            }
        case _:
            response = {
                'username': 'Unkown User',
                'weeks': [],
            }

    return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
