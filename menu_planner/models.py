from enum import Enum

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager

Base = declarative_base()


class StrEnum(str, Enum):
    """A Enum with elements that are strings."""


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    weeks = db.relationship('Week', backref='user', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        current_app.logger.debug('Password set for: %s', self.username)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        result = check_password_hash(self.password_hash, password)
        current_app.logger.debug('Password checked for: %s %s', self.username, result)
        return result


@login_manager.user_loader
def load_user(user_id: str) -> User:
    user = db.session.get(User, int(user_id))
    return user


class Week(Base):
    __tablename__ = 'weeks'

    def __repr__(self) -> str:
        return f'<Week {self.name} by User {self.user_id}>'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.Text, nullable=False)
    meals = db.relationship('Meal', backref='week', lazy='dynamic')

    def get_meals_by_days(self):
        result = {day: {meal_type: None for meal_type in Meal.MealType} for day in Meal.Day}
        for meal in self.meals:
            result[meal.day][meal.meal_type] = meal

        return result


class Meal(Base):
    __tablename__ = 'meals'

    class Day(StrEnum):
        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"
        SATURDAY = "Saturday"
        SUNDAY = "Sunday"

    class MealType(StrEnum):
        BREAKFAST = "Breakfast"
        LUNCH = "Lunch"
        SNACKS = "Snacks"
        DINNER = "Dinner"

    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey(Week.id), nullable=False)
    name = db.Column(db.Text, nullable=False)
    day = db.Column(db.Enum(Day), nullable=False)
    type = db.Column(db.Enum(MealType), nullable=False)
    picture = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f'<Meal {self.name} by ID {self.id}>'
