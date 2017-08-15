
from scraper import Scraper as sc
from pipelines import Pipeline as pp
from html_parser import HtmlParser as hp
import datetime


class Main_class():
    def main():
        sd = input("Start Date(yyyy,m,d): ")
        ed = input("End Date(yyyy,m,d): ")
        print(datetime.datetime.now())
        multiParsedTagList = hp.get_fullParsedTagList(sd, ed)
        tagSelect = sc.get_singlePageInfo(multiParsedTagList)
        pageInfos = sc.get_pageInfos(tagSelect)
        #pp.print_mergedList(pageInfos)
        pp.save_csv(pageInfos, sd, ed)
        print(datetime.datetime.now())

if __name__ == '__main__':
    Main_class.main()
