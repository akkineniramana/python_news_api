import os
import json
import datetime
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from newsapi import NewsApiClient
from .tasks.source_list import news_source
from .tasks.news_task import get_news
from datetime import date


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)



app = Flask(__name__)




app.config['MONGO_URI'] = os.environ.get('DB', 'mongodb://localhost:27017/newsAPI')
# app.config['MONGO_URI'] = os.environ.get('DB', 'mongodb://mbnadmin:nbm123!@mbn01-glqch.mongodb.net/newsAPI')
mongo = PyMongo(app)
app.json_encoder = JSONEncoder

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_news,args=[mongo], trigger="interval", minutes=1)
scheduler.start()
from app.controllers import *
