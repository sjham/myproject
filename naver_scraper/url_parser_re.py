
#from date_parser_re import DateParser as dp

class UrlParser():
    @classmethod
    def getDayUrls(cls, datesSet):
        initUrl = 'http://news.naver.com/main/history/mainnews/text.nhn?date='
        urls = []
        for i in datesSet:
            urls.append(initUrl+'{}&page='.format(i))
        print(urls)
        return urls
#
# if __name__ == '__main__':
#     sd = input("Start Date(yyyy,m,d): ")
#     ed = input("End Date(yyyy,m,d): ")
#     UrlParser.getDayUrls(dp.getDate(sd, ed))
