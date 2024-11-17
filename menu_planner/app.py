from flask import Flask, jsonify, request, session

from storage import db
from storage.models import User
from settings import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)


@app.route('/api/get_weeks', methods=['GET'])
def get_weeks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User unauthorized!'}), 401

    response = {
        'username': session['username'],
        # 'weeks': user.weeks,
    }
    return jsonify(response), 200


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Fetch user
    user: User = User.query.filter_by(email=email).one_or_none()
    if not user:
        return jsonify({'error': 'Invalid email'}), 409

    if not  user.check_password(password):
        return jsonify({'error': 'Invalid password'}), 409

    session['user_id'] = user.id
    session['username'] = user.username
    response = {
        'message': 'User logged in successfully',
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
        return jsonify({'error': 'User already exists'}), 409

    # Hash the password and store user
    user = User(username, email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username
    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    app.run('0.0.0.0', 8000)
