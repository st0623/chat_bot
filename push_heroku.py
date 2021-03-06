# coding: utf-8 
from apscheduler.schedulers.blocking import BlockingScheduler
import csv
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import getNikkeiHeadline
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort
from func.news.yahoo_news_rss import get_yahoo_news_list
from connect_sqlalchemy import get_news_list
import random

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)

line_id_list = []

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB接続に関する部分
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['NEWS_DATABASE_URL']
db = SQLAlchemy(app)

sched = BlockingScheduler()

class line_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.String(255), unique=True)

    def __init__(self, line_id):
        self.line_id = line_id

    def __repr__(self):
        return '<line_user %r>' % self.line_id


@sched.scheduled_job('interval', hours=6)# day_of_week='mon-fri', hour=21)

def push_news():
    user_db = db.session.query(line_user).all()
    line_id_list = []

    for v in user_db:
        line_id_list.append(v.line_id)

    print (line_id_list)
    newses= get_news_list()

    try:
        random_index = random.randint(0, len(newses))
        print (random_index)
        line_bot_api.multicast(line_id_list[1:], TextSendMessage(text=newses[random_index].get_news_str()))
    except LineBotApiError as e:
        print (e)

sched.start()
