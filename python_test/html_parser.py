
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen

class HtmlParser():

    @classmethod
    def urlParserBs4(cls, url, targetTag):
        #url = 'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-26&page=22'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser', from_encoding="cp949")
        tagSelect = soup.select(targetTag)
        #print(tagSelect)
        return tagSelect

    def get_tagparserBs4(cls, tagList, targetTag):
        soup = BeautifulSoup(tagList, 'html.parser', from_encoding="cp949")
        tagSelect = soup.select(targetTag)
        #print(tagSelect)
        return tagSelect

    @classmethod
    def get_tagList(cls, pageNum):
        urls = ['http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-28',
                'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-29'
                ]
        ht = HtmlParser()
        parseUrl = urls[0]+'&page={}'.format(pageNum)
        tagList = ht.urlParserBs4(parseUrl, 'ul.mlist2 > li')
        #tagList = soup.select('ul.mlist2 > li')
        #print(tagList)
        return tagList

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
    tagList = a.get_multiTagList(a.get_tagList)
    a.get_tagparserBs4(str(tagList), 'li')

    #a.get_multiTagList(a.get_tagList)
