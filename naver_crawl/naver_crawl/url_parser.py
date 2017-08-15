
class UrlParser():
    @classmethod
    def getDayUrls(cls, datesSet):
        initUrl = 'http://news.naver.com/main/history/mainnews/text.nhn?date='
        urls = []
        for i in datesSet:
            urls.append(initUrl+'{}&page='.format(i))
        return urls
