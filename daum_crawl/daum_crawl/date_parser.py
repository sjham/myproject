
from datetime import timedelta, datetime

class DateParser():
    @classmethod
    def getDate(cls, sd, ed):
        date1 = datetime.strptime(sd, "%Y,%m,%d")
        date2 = datetime.strptime(ed, "%Y,%m,%d")
        delta = date2 - date1
        datesSet = []
        for i in range(delta.days + 1):
            rawDates = date1 + timedelta(days=i)
            newsDates = str(rawDates).replace("00:00:00", "").rstrip()
            datesSet.append(newsDates)
        return datesSet

    @classmethod
    def getDayUrls(cls, datesSet):
        initUrl = 'http://media.daum.net/newsbox?tab_cate=NE&regDate='
        urls = []
        for i in datesSet:
            urls.append(initUrl+'{}'.format(i.repalce("-", "")))
        return urls

    #http://media.daum.net/newsbox?page=10&tab_cate=NE&regDate=20170801
    #
    # @classmethod
    # def getDayUrls(cls, datesSet):
    #     initUrl = 'http://m.news.naver.com/historyMainList.nhn?searchYmdt='
    #     urls = []
    #     for i in datesSet:
    #         urls.append(initUrl+'{}%2000:00#15&32700'.format(i))
    #     return urls
