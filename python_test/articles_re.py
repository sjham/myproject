
import html_parser_git_re
from scraper_re import Scraper as sc
from html_parser_git_re import HtmlParser as hp
import csv

class Pipeline():
    @classmethod
    def print_mergedList(cls, pageInfos):
        for item in pageInfos:
            print(item)

    @classmethod
    def save_csv(cls, pageInfos, sd, ed):
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_ver.csv"
        csvFile = open(tmpFile, 'wt', newline='')
        writer = csv.writer(csvFile)
        #writer.writerow(['news', 'source', 'expotime'])
        for item in pageInfos:
            writer.writerow(list(item))
    #
    # @classmethod
    # def save_mysql(cls, pageInfos):
    #


if __name__ == '__main__':
    a = Pipeline()
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    multiParsedTagList = hp.get_fullParsedTagList(sd, ed)
    tagSelect = a.get_singlePageInfo(multiParsedTagList)
    pageInfos = a.get_pageInfos(tagSelect)
    hp = html_parser_git_re.HtmlParser()
    multiParsedTagList = hp.get_multiParsedTagList(hp.get_ParsedTagList)
    tagSelect = sc.get_singlePageInfo(multiParsedTagList)
    pageInfos = sc.get_pageInfos(tagSelect)
    a.get_mergedList(pageInfos)
    a.save_csv(pageInfos)
