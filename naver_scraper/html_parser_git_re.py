
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
from date_parser_re import DateParser as dp
from url_parser_re import UrlParser as up

class HtmlParser():
    @classmethod
    def urlParserBs4(cls, url, targetTag):
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser', from_encoding="cp949")
        tagSelect = soup.select(targetTag)
        return tagSelect

    def get_tagparserBs4(cls, tagList, targetTag):
        soup = BeautifulSoup(tagList, 'html.parser', from_encoding="cp949")
        tagSelect = soup.select(targetTag)
        return tagSelect

    @classmethod
    def get_tagList(cls, pageNum):

        parsedUrl = cls.urls[0]+'{}'.format(pageNum)
        tagList = cls.urlParserBs4(parsedUrl, 'ul.mlist2 > li')
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
        print(multiTagList)
        return multiTagList

    @classmethod
    def get_multiParsedTagList1(cls, tagList_func):
        multiParsedTagList = []
        multiParsedTagList.append(tagList_func(1))
        for i in range(1, 30):
            if tagList_func(i) == tagList_func(i+1):
                break
            else:
                multiParsedTagList.append(tagList_func(i+1))
            time.sleep(2)
        print(multiParsedTagList)
        return multiParsedTagList

    @classmethod
    def get_ParsedTagList(cls, pageNum, url):
            parsedUrl = url+'{}'.format(pageNum)
            html = urlopen(parsedUrl)
            soup = BeautifulSoup(html, 'html.parser', from_encoding="cp949")
            tagSelect = soup.select('ul.mlist2 > li')
            return tagSelect

    @classmethod
    def get_multiParsedTagList(cls, tagList_func, url):
        yield tagList_func(1, url)
        for i in range(1, 30):
            if tagList_func(i, url) == tagList_func(i+1, url):
                break
            else:
                yield tagList_func(i+1, url)
            time.sleep(1)

    @classmethod
    def get_fullParsedTagList(cls, sd ,ed):
        a = HtmlParser()
        urls = up.getDayUrls(dp.getDate(sd, ed))
        for url in urls:
            fullParsedTagList = a.get_multiParsedTagList(a.get_ParsedTagList, url)
            yield fullParsedTagList
#
#
# if __name__ == '__main__':
#     a = HtmlParser()
#     sd = input("Start Date(yyyy,m,d): ")
#     ed = input("End Date(yyyy,m,d): ")
#     gen = a.get_fullParsedTagList(sd, ed)
#     tagSelect = (tagSelect for mt in gen for tagSelect in mt)
#     for i in tagSelect:
#         print(i)
