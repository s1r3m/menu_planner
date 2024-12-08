from urllib.parse import urlparse

from flask import Blueprint, Response, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from forms import LoginForm, RegistrationForm
from models import User, Week

routes = Blueprint('routes', __name__)


@routes.route('/')
@routes.route('/index')
def index() -> str:
    current_app.logger.debug('Index -- Main Page requested.')
    return render_template('index.html', login=True, signup=True)


@routes.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    current_app.logger.debug('Login -- Login Form requested.')
    if current_user.is_authenticated:
        current_app.logger.info('Login -- User logged in: %s', current_user.username)
        return redirect(url_for('routes.weeks'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if not (user and user.check_password(form.password.data)):
            current_app.logger.info('Login -- login failed: %s', form.username.data)
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


@routes.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    current_app.logger.debug('Registration -- registration requested.')
    if current_user.is_authenticated:
        current_app.logger.info('Register -- User logged in: %s', current_user.username)
        return redirect(url_for('routes.weeks'))

    form = RegistrationForm()
    current_app.logger.debug('Registration -- form is ready.')
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('Registration -- User added %s %s!', user.username, user.email)
        login_user(user)
        return redirect(url_for('routes.weeks'))
    current_app.logger.debug('GET Registration -- render template from form %s', form.hidden_tag())
    return render_template('register.html', login=True, form=form)


@routes.route('/weeks')
@login_required
def weeks() -> str | Response:
    current_app.logger.debug('Weeks for %s', current_user.username)
    weeks = db.session.query(Week).filter_by(user_id=current_user.id)
    weeks_data = [{'name': week.name} for week in weeks]
    current_app.logger.debug('weeks -- weeks %s', weeks_data)
    return render_template('weeks.html', weeks=weeks_data, logout=True)


@routes.route('/logout')
def logout() -> str | Response:
    logout_user()
    current_app.logger.info('Logout -- User logged out')
    return redirect(url_for('routes.index'))
