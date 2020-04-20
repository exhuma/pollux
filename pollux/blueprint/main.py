from datetime import datetime

from flask import Blueprint, g, jsonify, request
from pollux.datasource import DataSource

MAIN = Blueprint('', __name__)


@MAIN.before_app_request
def globals():
    ds = getattr(g, 'data_source', None)
    if not ds:
        ds = DataSource.default()
        g.data_source = ds


@MAIN.after_app_request
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@MAIN.route('/')
def index():
    return jsonify({
        '_links': {
            'recent': {
                'href': '/recent',
                'title': 'Fetch data for the last <n> days'
            }
        }
    })


@MAIN.route('/recent')
def recent():
    num_days = int(request.args.get('num_days', 7))
    genera = request.args.getlist('genus')
    print(genera)
    data = g.data_source.recent(num_days=num_days, genera=genera)
    return jsonify(data)


@MAIN.route('/between/<start>/<end>')
def between(start, end):
    startDate = datetime.strptime(start, '%Y-%m-%d')
    endDate = datetime.strptime(end, '%Y-%m-%d')
    genera = request.args.getlist('genus')
    data = g.data_source.between(startDate, endDate, genera=genera)
    return jsonify(data)
