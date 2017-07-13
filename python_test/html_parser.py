
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import date_parser

class HtmlParser():

    # def urlParser(cls, url):
    #     initUrl = 'http://news.naver.com/main/history/mainnews/text.nhn?date='
    #     getStartDate = input(date)


    @classmethod
    def urlParserBs4(cls, urls, targetTag):
        #url = 'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-26&page=22'
        for url in urls:
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser', from_encoding="cp949")
            tagSelect = soup.select(targetTag)
            yield tagSelect
        #print(tagSelect)
        #return tagSelect

    @classmethod
    def get_tagparserBs4(cls, tagList, targetTag):
        soup = BeautifulSoup(tagList, 'html.parser', from_encoding="cp949")
        tagSelect = soup.select(targetTag)
        #print(tagSelect)
        return tagSelect

    @classmethod
    def get_tagList(cls, urls, pageNum):

        hp = HtmlParser()
        parseUrl = urls[0]+'{}'.format(pageNum)
        tagList = hp.urlParserBs4(parseUrl, 'ul.mlist2 > li')
        return tagList

        #
        #
        # tagtotal=[]
        #
        # for url in urls:
        #     i=1
        #
        #     for i in range(12):
        #         parseUrl = urls[0]+'{}'.format(pageNum)
        #         tagList = hp.urlParserBs4(parseUrl, 'ul.mlist2 > li')
        #         tagtotal.append(tagList)
        #         i+=1
        # hp = HtmlParser()
        # tagtotal=[]
        # for url in urls:
        #     i=1
        #     for i in range(12):
        #         parseUrl = urls+'{}'.format(i)
        #         tagList = hp.urlParserBs4(parseUrl, 'ul.mlist2 > li')
        #         tagtotal.append(tagList)
        #         i+=1
        # hp = HtmlParser()
        # parseUrl = urls+'{}'.format(pageNum)
        # tagList = hp.urlParserBs4(parseUrl, 'ul.mlist2 > li')
        #tagList = soup.select('ul.mlist2 > li')
        # print(tagtotal)
        # return tagtotal
        #return tagList

    @classmethod
    def get_multiTagList(cls, tagList_func):
        multiTagList = []
        multiTagList.append(tagList_func(1))
        for i in range(1, 30):
            if tagList_func(i) == tagList_func(i+1):
                break
            else:
                multiTagList.append(tagList_func(i+1))
            time.sleep(1)
        #print(multiTagList)
        return multiTagList

if __name__ == '__main__':
    a = HtmlParser()
    # url = 'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-26&page=22'
    # a.urlParserBs4(url, 'li')
    #a.get_tagList(1)
    dp = date_parser.DateParser()
    urls = dp.getUrls(dp.getDate())

    #a.get_tagList(urls)

    tagList = a.get_multiTagList(a.get_tagList)
    a.get_tagparserBs4(str(tagList), 'li')
    # a.get_tagparserBs4(str(tagList), 'li')

    a.get_multiTagList(a.get_tagList(urls))
