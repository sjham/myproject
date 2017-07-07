from bs4 import BeautifulSoup
from urllib.request import urlopen
#from html_parser import *
import html_parser

class Scraper():
    #@classmethod
    # def __init__(self, title, source, expotime):
    #     self.title = title
    #     self.source = source
    #     self.expotime = expotime
    #     #self.url = url

    @classmethod
    # def get_pageInfos(cls, tagSelect):
    #
    #     # soup = BeautifulSoup(tagSelect, 'html.parser')
    #     # scrap = soup.select('li')
    #     titles = [[item.find('a').text.strip()] for item in tagSelect]
    #     sources = [[item.find(attrs={'class': 'writing'}).text.strip()] for item in tagSelect]
    #     expotimes_ex = [item.findAll(attrs={'class': 'eh_edittime'}) for item in tagSelect]
    #     #expotimes = [[sh.text.strip() for sh in expotimes_ex for val in sh]]
    #     #print(expotimes)
    #     print(titles, sources, expotimes_ex)

    def get_pageInfos(self, tagSelect):
        # soup = BeautifulSoup(tagSelect, 'html.parser')
        # scrap = soup.select('li')
        for item in tagSelect:
            self.title = [item.find('a').text.strip()]
            #[item.find(attrs={'class': 'writing'}).text.strip()]
            self.source = [item.find(attrs={'class': 'writing'}).text.strip()]
            expotimes_ex = item.findAll(attrs={'class': 'eh_edittime'})
            for sh in expotimes_ex:
                self.expotime = [sh.text.strip()]

            #print(self.title, self.source, self.expotime)
            yield(self.title, self.source, self.expotime)
            # for i in a:
            #     print(i)


if __name__ == '__main__':
    a = Scraper()
    b = html_parser.HtmlParser()
    multiTagList = b.get_multiTagList(b.get_tagList)
    tagSelect = b.get_tagparserBs4(str(multiTagList), 'li')
    # print(tagSelect)
    a.get_pageInfos(tagSelect)

    #b.get_tagparserBs4
    #print(multiTagList)
    #multiTagList = """<li><a href="http://news.naver.">골프연습장서 외제차 탄 주부 납치 살해</a></li>"""

    #a.get_pageInfos(str(multiTagList))
    # b = html_parser.HtmlParser()
    # targetElements = b.get_multiElements(b.get_targetElement)
    # a.get_pageInfos(targetElements)
