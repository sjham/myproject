# -*- coding: utf-8 -*-
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
            stripedDates = newsDates.replace("-", "")
            datesSet.append(stripedDates)
            # datesSet.append(newsDates)
        return datesSet

    @classmethod
    def getDayUrls(cls, datesSet):
        initUrl = 'http://news.naver.com/main/history/mainnews/text.nhn?date='
        urls = []
        for i in datesSet:
            urls.append(initUrl+'{}&page='.format(i))
        return urls
