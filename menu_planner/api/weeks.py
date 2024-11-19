from flask import Blueprint, jsonify, make_response

weeks_api = Blueprint('weeks_api', __name__)


@weeks_api.route('/api/get_weeks', methods=['GET'])
def get_weeks():
    weeks = [{'name': 'Week 1'}, {'name': 'Xmas Week'}]
    return make_response(jsonify(weeks), 200)
