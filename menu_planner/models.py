from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    def __init__(self, username: str) -> None:
        self.username = username

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    def set_password(self, password: str) -> None:
        current_app.logger.debug('Models set_password-- Password set for: %s', self.username)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        result = check_password_hash(self.password_hash, password)
        current_app.logger.debug('Models -- Password checked for: %s %s', self.username, result)
        return result


@login_manager.user_loader
def load_user(id: str) -> User:
    user = db.session.get(User, int(id))
    current_app.logger.debug('Models load_user -- User loaded: %s', user)
    return user


class Week(db.Model):
    __tablename__ = 'weeks'

    def __init__(self, user: User, name: str) -> None:
        self.user_id = user.id
        self.name = name

    def __repr__(self) -> str:
        return f'<Week {self.name} by User {self.user_id}>'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.Text, nullable=False)
