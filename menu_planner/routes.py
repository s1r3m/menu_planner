from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template('index.html', login=True, signup=True)


@routes.route('/weeks')
def weeks():
    weeks_data = [{'name': 'Week 1'}, {'name': 'Xmas Week'}]
    return render_template('weeks.html', weeks=weeks_data, logout=True)

@routes.route('/logout')
def logout():
    # Drop all sessions an so on
    return render_template('index.html', login=True, signup=True)
