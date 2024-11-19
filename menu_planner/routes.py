from pathlib import Path

from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

TEMPLATE_PATH = Path(__file__).parent / 'templates'

@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/weeks')
def weeks():
    weeks_data = [{'name': 'Week 1'}, {'name': 'Xmas Week'}]
    return render_template('weeks.html', weeks=weeks_data)
