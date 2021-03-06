from bs4 import BeautifulSoup
from urllib.request import urlopen
import html_parser_git

import date_parser

class Scraper():
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
    b = html_parser_git.HtmlParser()
    #dp = date_parser.DateParser()
    #urls = dp.getDayUrls(dp.getDate())
    multiParsedTagList = b.get_multiParsedTagList(b.get_ParsedTagList)
    tagSelect = multiParsedTagList
    a.get_pageInfos(tagSelect)
