import os
from flask import request, jsonify
from app import app, mongo
import logger
from datetime import date, timedelta
import json
from bson.json_util import dumps

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/news', methods=['GET'])
def news():
    if "search" in request.args:
        search_string = request.args.get('search')
        data = []
        if search_string is not None:
            data = dumps(mongo.db.news.find(
            {"description": {'$regex': search_string, "$options" : "-i"}}))
        return jsonify(json.loads(data)), 200
    else:
        d = request.args.get('date')
        if d is None:
            d = date.today()
            d = d.strftime("%Y-%m-%d")
        data = dumps(mongo.db.news.find({"publishedAt": { '$regex' : d}}))
        return jsonify(json.loads(data)), 200
