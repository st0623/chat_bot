# coding: utf-8 
import csv
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import getNikkeiHeadline
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi('channel_access_token')

line_id_list = []

app = Flask(__name__)
# DB接続に関する部分
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# モデル作成
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_userid = db.Column(db.String(80), unique=True)

    def __init__(self, line_userid):
        self.line_userid = line_userid

    def __repr__(self):
        return '<Users %r>' % self.line_userid


# with open('line_id.csv') as f:
#     reader = csv.reader(f)
#    header = next(reader)

user_db = db.session.query(Users).all()
line_id_list = []
for v in user_db:
    line_id_list.append(v.line_userid)
nikkei = getNikkeiHeadline.getNikkeiHeadline()
title_list = nikkei.getTitle()
url_list = nikkei.getUrl()
try:
    line_bot_api.multicast(line_id_list, TextSendMessage(text=title_list[0] + "\n https://www.nikkei.com"+url_list[0]))
except LineBotApiError as e:
    # error handle
    ...

