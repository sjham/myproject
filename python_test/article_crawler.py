from datetime import timedelta, datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from input_value import InputValue

class Article_crawler():
    #def __init__(self, title, source, expotime, url):
    def __init__(self):
        pass
        # self.title = title
        # self.source = source
        # self.expotime = expotime
        # self.url = url

    @classmethod
    def get_datesSet(cls, inputValue):
        #inputValue = InputValue("2017,6,25", "2017,6,26")
        delta = inputValue.endDate - inputValue.startDate
        datesSet = []
        for i in range(delta.days + 1):
            rawDates = inputValue.startDate + timedelta(days=i)
            datesSet.append(str(rawDates).replace("00:00:00", "").rstrip())
        print(datesSet)
        return datesSet

    @classmethod
    def get_urls(cls, datesSet):
        #datesSet = ['2017-06-25', '2017-06-26']
        start_url = 'http://news.naver.com/main/history/mainnews/text.nhn?date='
        urls = []
        for date in datesSet:
            urls.append(start_url+'&page={}'.format(date))
        print(urls)
        return urls

    @classmethod
    def get_initUrls(cls, datesSet):
        initUrls = []
        for i in datesSet:
            urls.append("http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i)
        return initUrls

    @classmethod
    def get_pageNum(cls, urls):
        maxNum = []
        for url2 in urls:
            html = urlopen(url2)
            soup = BeautifulSoup(html, 'html.parser')
            exmaxNum = soup.select("div.mtype_list_wide > div.eh_navi > div:nth-of-type(1)")[0].text
            splitNum = exmaxNum.split('/')
            maxNum.append(int(splitNum[1]))
        print(maxNum)
        return maxNum

    @classmethod
    def get_pageTitles(cls, pageNum):
        # urls = ['http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-28',
        #         'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-29'
        #         ]
        html = urlopen(urls[0]+'&page={}'.format(pageNum))
        time.sleep(1)
        #print(urls[0]+'&page={}'.format(pageNum))
        soup = BeautifulSoup(html, 'html.parser', from_encoding="cp949")
        scrap = soup.select('ul.mlist2 > li')
        pageTitles = ([item.find('a').text.strip()] for item in scrap)

        #print(pageTitles)
        for generator in pageTitles:
            print(generator)

    @classmethod
    def get_multiPageTitles(cls, pageTitles_func):
        print("multi start print")
        multiPageTitles = (pageTitles_func(i) for i in range(1, 17))
        print("multi end print")
        y = []
        for item in list(multiPageTitles)[1:]:
            if item == list(pageTitles_func(1))[0]:
                break
            else:
                y.append(item)
        print(y)
        #
        #         yield item
        # for t in item:
        #     print(t)
        # for generator in multiPageTitles:
        #     print(generator)


if __name__ == '__main__':
    a = Article_crawler()
    urls = ['http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-28',
            'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-29'
            ]
    inputValue = InputValue("2017,6,25", "2017,6,26")
    a.get_datesSet(inputValue)
    a.get_urls(a.get_datesSet(inputValue))
    a.get_initUrls(a.get_datesSet(inputValue))
    #a.get_pageNum(a.get_urls(a.get_datesSet(inputValue)))

    a.get_multiPageTitles(a.get_pageTitles)
