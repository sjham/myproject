#
# import html_parser_git_re
# from scraper_re import Scraper as sc
#from html_parser_git_re import HtmlParser as hp
# import itertools
import csv

class Pipeline():
    @classmethod
    def print_mergedList(cls, pageInfos):
        for item in pageInfos:
            print(item)

    @classmethod
    def save_csv(cls, pageInfos, sd, ed):
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_{}_to_{}.csv".format(sd, ed)
        #tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_ver.csv"
        csvFile = open(tmpFile, 'wt', newline='')
        writer = csv.writer(csvFile)
        writer.writerow(['title', 'source', 'expotime'])
        for item in pageInfos:
            print(item)
            writer.writerow(item)
        csvFile.close()


    # def save_csv(cls):
    #     #tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_{}_to_{}.csv".format(sd, ed)
    #     tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_ver.csv"
    #     with open(tmpFile, 'wt', newline='') as csvFile:
    #         writer = csv.writer(csvFile)
    #         writer.writerow(['title', 'source', 'expotime'])
    #         item = ('특검, 최종 수사결과 6일 발표… 탄핵심판에 영향?', '세계일보', ['03/01 19:12 ~ 03/02 05:10 (9시간58분) 노출'])
    #
    #         writer.writerow(item)
#
# if __name__ == '__main__':
#     a = Pipeline()
#     a.save_csv()
# #     sd = input("Start Date(yyyy,m,d): ")
# #     ed = input("End Date(yyyy,m,d): ")
#     multiParsedTagList = hp.get_fullParsedTagList(sd, ed)
# #     tagSelect = sc.get_singlePageInfo(multiParsedTagList)
# #     pageInfos = sc.get_pageInfos(tagSelect)
# #     a.save_csv(pageInfos)
