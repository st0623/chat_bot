from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('mQrjT6U8PbTD5w+SVFwTMgh+0qFNlfRotWhl3GVgw55ZLAKA8w/kRJrI5bnoBR4AtQ1/FtuOow8E1kmE4dnpn1JKXneyQ9Imz/7vvwO5irRsUA3vKTzNnAMFTYMocQ503zT3/0oerQgZEcM1MY23igdB04t89/1O/w1cDnyilFU=')

try:
    line_bot_api.push_message('Uf2ec39b1cbe0581d53245b3962ef4f7f', TextSendMessage(text='Hello World!'))
except LineBotApiError as e:
    # error handle
    ...

