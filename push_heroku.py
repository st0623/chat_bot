# coding: utf-8 
import csv
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import getNikkeiHeadline
import os

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi('channel_access_token')

line_id_list = []

# DB接続に関する部分
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


# with open('line_id.csv') as f:
#     reader = csv.reader(f)
#    header = next(reader)

    user_db = db.query(Users).all()
    user_id_list = []
    for v in user_db:
        user_id_list.append(v.line_userid)
    nikkei = getNikkeiHeadline.getNikkeiHeadline()
    title_list = nikkei.getTitle()
    url_list = nikkei.getUrl()
    for row in reader:
        line_id_list.append(row[1])
try:
    line_bot_api.multicast(line_id_list, TextSendMessage(text=title_list[0] + "\n https://www.nikkei.com"+url_list[0]))
except LineBotApiError as e:
    # error handle
    ...

