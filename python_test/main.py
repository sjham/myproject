import html_parser_git_re
from scraper_re import Scraper as sc
from articles_re import Pipeline as ap


class Main_class():
    @classmethod
    def main(cls):
        hp = html_parser_git_re.HtmlParser()
        multiParsedTagList = hp.get_multiParsedTagList(hp.get_ParsedTagList)
        tagSelect = sc.get_singlePageInfo(multiParsedTagList)
        pageInfos = sc.get_pageInfos(tagSelect)
        ap.get_mergedList(pageInfos)
        ap.save_csv(pageInfos)

if __name__ == '__main__':
    Main_class.main()
