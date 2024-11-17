from flask import Flask, request, jsonify

from models import User, db

app = Flask(__name__)

# Define mock user data
users_data = {
    'santa_clause': [
        {'name': 'Week 1'},
        {'name': 'Xmas Week'},
    ],
    'Filipp': [],  # No weeks added for Filipp
}

@app.route('/api/get_weeks', methods=['GET'])
def get_weeks():
    button_name = ''
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


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Fetch user
    user = User.query.filter_by(email=email).one_or_none()
    if not (user and user.check_password(password)):
        return jsonify({'error': 'Invalid email or password'}), 401

    response = {
        'username': user.username,
        'email': user.email,
    }
    return jsonify(response), 200


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    # Check if user exists
    user = User.query.filter_by(email=email).one_or_none()
    if user:
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password and store user
    user = User(username, email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
