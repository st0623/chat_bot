import urllib.request, urllib.error
from bs4 import BeautifulSoup

class getNikkeiHeadline():
    ''' 日経の主要ニュースのタイトルとURL取得 '''
    def __init__(self):
        self.url = "http://www.nikkei.com/news/headline/archive/"

        self.html = urllib.request.urlopen(self.url)

        self.soup = BeautifulSoup(self.html, "html.parser")

    def getTitle(self):
        ''' タイトルを取得 '''
        spans = self.soup.find_all("span")

        nikkei_headline_title = []

        for span in spans:
            try:
                string_ = span.get("class").pop(0)

                if string_ in ["cmnc-middle", "cmnc-small"]:
                    nikkei_headline_title.append(span.string)

            except:
                pass

        return nikkei_headline_title


    def getUrl(self):
        ''' ニュースのURLを取得 '''
        a_tags = self.soup.find_all("a")
        nikkei_news_url = []

        for a_tag in a_tags:
            try:
                if a_tag.get("href").startswith("/article/DGX"):
                    nikkei_news_url.append(a_tag.get('href'))

            except:
                pass


        return nikkei_news_url


gnh = getNikkeiHeadline()
title_list = gnh.getTitle()
url_list = gnh.getUrl()
'''
for title, url in zip(title_list, url_list):
    print ("---------------")
    print (title + " : ")
    print ("https://www.nikkei.com" + url)

print (type(title_list))
'''
