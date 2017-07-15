
import itertools
#from html_parser_git_re import HtmlParser as hp

class Scraper():
    @classmethod
    def get_singlePageInfo(self, multiParsedTagList):
        tagSelect1 = itertools.chain.from_iterable(multiParsedTagList)
        tagSelect = itertools.chain.from_iterable(tagSelect1)
        return tagSelect

    @classmethod
    def get_pageInfos(self, tagSelect):
        for item in tagSelect:
            title = item.find('a').text.strip()
            source = item.find(attrs={'class': 'writing'}).text.strip()
            expotimes_ex = item.findAll(attrs={'class': 'eh_edittime'})
            expotime = [sh.text.strip() for sh in expotimes_ex]
            yield(title, source, expotime)
#
# if __name__ == '__main__':
#     a = Scraper()
#     sd = input("Start Date(yyyy,m,d): ")
#     ed = input("End Date(yyyy,m,d): ")
#     multiParsedTagList = hp.get_fullParsedTagList(sd, ed)
#     tagSelect = a.get_singlePageInfo(multiParsedTagList)
#     pageInfos = a.get_pageInfos(tagSelect)
#     for i in pageInfos:
#         print(i)
    #a.get_pageInfos(tagSelect)
