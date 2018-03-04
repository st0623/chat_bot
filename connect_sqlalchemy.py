import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import select 

def get_news_list():
    url = 'postgresql://mvzgskipdsvaxp:6537b5845d6ce23156e60e7105bf3f9648baa097cf7208db697fcb56c53abc0e@ec2-174-129-26-203.compute-1.amazonaws.com:5432/d9ulhkpdiac7bc'
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

    return executeResult


