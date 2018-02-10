## -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import json
from argparse import ArgumentParser

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,FollowEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


# DB接続に関する部分
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

# DB接続に関する部分
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# モデル作成
class Users(db.models):
    id = db.Column(db.Integer, primary_key=True)
    line_userid = db.Column(db.String(80), unique=True)

    def __init__(self, line_userid):
        self.line_userid = line_userid

    def __repr__(self):
        return '<Users %r>' % self.line_userid


# flaskによるマッピング
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #receive_json = json.loads(body)
    #userId = receive_json["events"][0]["source"]["userId"]
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def get_userid():
    body = request.get_data(as_text=True)
    receive_json = json.loads(body)
    userId = receive_json["events"][0]["source"]["userId"]
    return userId

@handler.add(FollowEvent)
def follow(event):
    line_userId = get_userid()
    # emailが未登録ならユーザー追加
    if not db.session.query(Users).filter(Users.line_userid == line_userId).count():
        reg = Users(line_userId)
        db.session.add(reg)
        db.session.commit()
    follow_message = "友達登録ありがとう!\n毎日最新のニュースをプッシュします"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=follow_message)
    )

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    body = request.get_data(as_text=True)
    receive_json = json.loads(body)
    #userId = receive_json["events"][0]["source"]["userId"]

    event_list = receive_json["events"]
    userId = "hogehoge"
    for e in event_list:
        if e["type"] == "follow":
            userId = e["source"]["userId"]
            break

    # receive_json = json.loads(MessageEvent)
    # userId = receive_json["events"][0]["source"]["userId"]
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=userId)
    )
        ## TextSendMessage(text=event.message.text)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
