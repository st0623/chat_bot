class News:
    def __init__(self):
        self.column_list = ["id","url","title","overview","posted_at","category"]
        self.news_dict = {cl: "" for cl in self.column_list}

    def set_news(self, news_list):
        if len(self.column_list) != len(self.news_dict):
            print ("no match len")
            return False 

        for idx, cl in enumerate(self.column_list):
            self.news_dict[self.column_list[idx]] = news_list[idx]

        return True


    def get_news(self):
        return self.column_list

    def get_news_str(self):
        news_str = ""
        for key, value in self.news_dict.items():
            news_str += key + "\t" + str(value) + "\n"


        return news_str

