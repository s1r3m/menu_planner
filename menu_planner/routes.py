from urllib.parse import urlparse

from flask import Blueprint, Response, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from forms.login import LoginForm
from extensions import db
from models import User, Week

routes = Blueprint('routes', __name__)


@routes.route('/')
@routes.route('/index')
def index() -> str:
    return render_template('index.html', login=True, signup=True)


@routes.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    if current_user.is_authenticated:
        current_app.logger.info('Login -- User logged in: %s', current_user.username)
        return redirect(url_for('routes.weeks'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if not (user and user.check_password(form.password.data)):
            current_app.logger.debug('Login -- login failed: %s', form.username.data)
            form.password.error = 'Invalid username or password'
            return render_template('login.html', signup=True, form=form)

        login_user(user, remember=form.remember_me.data)
        current_app.logger.info('Login -- user logged %s', user.username)
        next_page = request.args.get('next')
        current_app.logger.debug('Login -- next page %s', next_page)
        if not next_page or urlparse(next_page).netloc != '':
            next_page = 'weeks'
        current_app.logger.debug('Login -- next page after: %s', next_page)
        return redirect(url_for(f'routes.{next_page}'))

    return render_template('login.html', signup=True, form=form)


@routes.route('/weeks')
@login_required
def weeks() -> str | Response:
    current_app.logger.debug('Weeks for %s', current_user.username)
    weeks = db.session.query(Week).filter_by(user_id=current_user.id)
    weeks_data = [{'name': week.name} for week in weeks]
    current_app.logger.debug('weeks -- weeks %s', weeks_data)
    return render_template('weeks.html', weeks=weeks_data, logout=True)


@routes.route('/register', methods=['GET', 'POST'])
def register() -> Response:
    if current_user.is_authenticated:
        current_app.logger.info('Register -- User logged in: %s', current_user.username)
        return redirect(url_for('routes.index'))

    user = db.session.query(User).filter_by(username='Vasya').first()
    if user:
        current_app.logger.debug('Register -- Vasya already added! Now update weeks')
        current_app.logger.debug('Register -- %s loaded from db', user.username)
        week_1 = Week(user=user, name='Week 1')
        week_2 = Week(user=user, name='Xmas Week')
        current_app.logger.debug('Register -- %s %s', week_1, week_2)
        db.session.add(week_1)
        db.session.add(week_2)
        db.session.commit()
        current_app.logger.info('Register -- Weeks added')
        login_user(user, remember=True)
        return redirect(url_for('routes.weeks'))

    user = User(username='Vasya')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    current_app.logger.debug('Register -- Vasya added!')

    return redirect(url_for('routes.login'))


@routes.route('/logout')
def logout() -> str | Response:
    logout_user()
    current_app.logger.info('Logout -- User logged out')
    return redirect(url_for('routes.index'))
