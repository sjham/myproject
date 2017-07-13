from bs4 import BeautifulSoup
from urllib.request import urlopen
from html_parser_git_re import HtmlParser as hp
#from date_parser_re import DateParser as dp
import html_parser_git_re

class Scraper():
    @classmethod
    def get_singlePageInfo(self, multiParsedTagList):
        for t in multiParsedTagList:
            #print(t)
            for tagSelect in t:
                yield tagSelect

    @classmethod
    def get_pageInfos(self, tagSelect):
        for item in tagSelect:
            self.title = [item.find('a').text.strip()]
            self.source = [item.find(attrs={'class': 'writing'}).text.strip()]
            expotimes_ex = item.findAll(attrs={'class': 'eh_edittime'})
            for sh in expotimes_ex:
                self.expotime = [sh.text.strip()]
            yield(self.title, self.source, self.expotime)

if __name__ == '__main__':
    a = Scraper()
    multiParsedTagList = hp.get_multiParsedTagList(hp.get_ParsedTagList)
    tagSelect = a.get_pageInfos(multiParsedTagList)
    a.get_pageInfos(tagSelect)
