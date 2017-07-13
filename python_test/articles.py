import html_parser_git
import scraper

class Articles():
    #@classmethod
    # def __init__(self, title, source, expotime):
    #     self.title = title
    #     self.source = source
    #     self.expotime = expotime
        #self.url = url

    @classmethod
    def get_mergedList(cls, pageInfos):
        #mergedList = []
        for item in pageInfos:
            print(item)
    #         mergedList.append(item)
    #     print(mergedList)
    # #
    # pageInfos = c.get_pageInfos(tagSelect)
    # a = Articles()
    #

if __name__ == '__main__':
    a = Articles()
    b = html_parser_git.HtmlParser()
    c = scraper.Scraper()

    #multiTagList = b.get_multiTagList(b.get_tagList)
    multiParsedTagList = b.get_multiParsedTagList(b.get_ParsedTagList)
    tagSelect = b.get_tagparserBs4(str(multiParsedTagList), 'li')
    #pageInfos = c.get_pageInfos(tagSelect)
    pageInfos = c.get_pageInfos(tagSelect)
    a.get_mergedList(pageInfos)

#    pageInfos = c.get_pageInfos(tagSelect)
    #
    # c.get_pageInfos(tagSelect)
    # c.get_pageInfos
    #
    # def get_pageInfos(self, tagSelect):
    #
