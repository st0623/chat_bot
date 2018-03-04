import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import select 
import os 
from news_table import News


def get_news_list():
    
    url = os.environ["NEWS_DATABASE_URL"]

    engine = sa.create_engine(url)
    session = sessionmaker(bind=engine)()
    conn = engine.connect()
     

# MetaData の生成
    meta = MetaData()


# Engineに結びつける
    meta.bind = engine 

    sample_table = Table('news', meta, autoload=True)
# 全検索の定義および実行
    selectQuery = select([sample_table])
    executeResult = conn.execute(selectQuery).fetchall()

    
    return list2News(executeResult)

def list2News(news_list):
    newses = []
    for nl in news_list:
        tmp_news = News()
        tmp_news.set_news(nl)
        newses.append(tmp_news)

    return newses

