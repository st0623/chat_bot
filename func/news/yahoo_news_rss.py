import feedparser

def get_yahoo_news_list():
    RSS_URL = "https://news.yahoo.co.jp/pickup/rss.xml"
    yahoo_news_dic = feedparser.parse(RSS_URL)


    news_list = []

    for entry in yahoo_news_dic.entries:
        news_list.append([entry.title, entry.published, entry.link])

    print (news_list)
    return news_list 
    

get_yahoo_news_list()
