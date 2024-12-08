from http import HTTPStatus
from urllib.parse import urlparse

from flask import abort, Blueprint, current_app, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from forms import LoginForm, RegistrationForm
from models import User, Week

routes = Blueprint('routes', __name__)


@routes.before_request
def before_request():
    if current_user.is_authenticated:
        g.user_data = {
            'name': current_user.username,
            'email': current_user.email,
        }
    else:
        g.user_data = {}


@routes.route('/meals')
def meals():
    pass


@routes.route('/')
@routes.route('/index')
def index():
    current_app.logger.debug('Index -- Main Page requested.')
    return render_template('index.html', login=True, signup=True)


@routes.route('/login', methods=['GET', 'POST'])
def login():
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
def register():
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
        return redirect(url_for('routes.weeks')), HTTPStatus.CREATED
    current_app.logger.debug('GET Registration -- render template from form %s', form.hidden_tag())
    return render_template('register.html', login=True, form=form)


@routes.route('/weeks')
@login_required
def weeks():
    current_app.logger.debug('Weeks for %s', current_user.username)
    weeks = db.session.query(Week).filter_by(user_id=current_user.id).all()
    if not weeks:
        test_week = Week(user_id=current_user.id, name='Test week')
        db.session.add(test_week)
        db.session.commit()
        weeks = [test_week]
    current_app.logger.debug('weeks -- weeks %s', weeks)
    return render_template('weeks.html', weeks=weeks)


@routes.route('/<username>/week/<name>')
@login_required
def week(username: str, name: str):
    if current_user.username != username:
        current_app.logger.debug('Week -- Wrong user %s for week %s', current_user.username, name)
        abort(HTTPStatus.NOT_FOUND)

    week: Week = db.session.query(Week).filter_by(user_id=current_user.id, name=name).first()
    if not week:
        current_app.logger.debug('Week -- No week %s in db', name)
        abort(HTTPStatus.NOT_FOUND)

    current_app.logger.debug('Week -- Week %s for %s', week.name, week.user.username)
    meals = week.get_meals_by_days()
    return render_template('week.html', week=week, data=meals)


@routes.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
    current_app.logger.debug('Page not found: %s', e)
    return render_template('404.html'), 404


@routes.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    current_app.logger.exception('Internal Server Error: %s', e)
    return render_template('500.html'), 500


@routes.route('/logout')
def logout():
    logout_user()
    current_app.logger.info('Logout -- User logged out')
    return redirect(url_for('routes.index'))
