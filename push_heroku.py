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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB接続に関する部分
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['NEWS_DATABASE_URL']
db = SQLAlchemy(app)

sched = BlockingScheduler()

# モデル作成
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_userid = db.Column(db.String(80), unique=True)

    def __init__(self, line_userid):
        self.line_userid = line_userid

    def __repr__(self):
        return '<Users %r>' % self.line_userid


@sched.scheduled_job('interval', minutes=2)# day_of_week='mon-fri', hour=21)
def push_news():
    user_db = db.session.query(Users).all()
    line_id_list = []

    for v in user_db:
        line_id_list.append(v.line_userid)

    newses= get_news_list()

    try:
        random_index = random.randint(0, len(newses))
        print (random_index)
        line_bot_api.multicast(line_id_list, TextSendMessage(text=newses[random_index].get_news_str()))
    except LineBotApiError as e:
        print (e)

sched.start()
