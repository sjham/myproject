import html_parser_git_re
from scraper_re import Scraper as sc
import csv

class Pipeline():

    @classmethod
    def get_mergedList(cls, pageInfos):
        for item in pageInfos:
            print(item)

    @classmethod
    def save_csv(cls, pageInfos):
        # n = sd.replace(',', '_')
        # n1 = ed.replace(',', '_')
        #tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s.csv" % (n, n1)
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews.csv"
        csvFile = open(tmpFile, 'wt', newline='')
        writer = csv.writer(csvFile)
        #writer.writerow(['news', 'source', 'expotime'])
        for item in pageInfos:
            writer.writerow(item)




if __name__ == '__main__':
    a = Pipeline()
    hp = html_parser_git_re.HtmlParser()
    multiParsedTagList = hp.get_multiParsedTagList(hp.get_ParsedTagList)
    tagSelect = sc.get_singlePageInfo(multiParsedTagList)
    pageInfos = sc.get_pageInfos(tagSelect)
    a.get_mergedList(pageInfos)
    a.save_csv(pageInfos)
