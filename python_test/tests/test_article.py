
import unittest

from article_crawler import Article_crawler
from input_value import InputValue

class Article_crawlerTest(unittest.TestCase):
    def setUp(self):

        pass

    def test_get_datesSet_success(self):
        inputValue = InputValue("2017,6,25", "2017,6,26")
        datesSet = Article_crawler.get_datesSet(inputValue)
        self.assertEqual(datesSet, ['2017-06-25', '2017-06-26'])
    #
    # def test_getDatesSet_fail(self):
    #     inputValue = InputValue("2017,6,26", "2017,6,25")
    #     datesSet = Article_crawler.getDatesSet(inputValue)
    #     self.assertEqual(datesSet, ["2017-06-25", "2017-06-26"])


    def test_get_urls_success(self):
        datesSet = ['2017-06-25', '2017-06-26']
        wantedurls = [
            'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-25&page=',
            'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-26&page=',
            ]
        urls = Article_crawler.get_urls(datesSet)
        self.assertEqual(urls, wantedurls)

    # def test_get_parsedHtml(self):
    #     #html = 'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-26&page=1'
    #     #html = 'http://news.naver.com/main/history/mainnews/list.nhn?date=2017-06-01'
    #     wantedNum = 10
    #     maxNum = Article_crawler.get_parsedHtml()
    #     self.assertEqual(maxNum, wantedNum)
    #
    # def test_scrap_info(self):
    #     urls = ['http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-28',
    #             'http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-29'
    #             ]
    #     wantedTitle = ['일선 판사 목소리 실린 사법개혁 시동']
    #     titles = Article_crawler.scrap_info(urls)
    #     self.assertEqual(titles[0], wantedTitle)
    #     wantedhtml='http://news.naver.com/main/history/mainnews/text.nhn?date=2017-06-29&page=1'
    #     html = Article_crawler.scrap_info()
    #     self.assertEqual(html, wantedhtml)
    # # def test_scrap_info(self):
    #
    # def test_scrap_info(self):
    #     currentTitles = Article_crawler.scrap_info()
    #     wantedTitle = ['일선 판사 목소리 실린 사법개혁 시동']
    #
    #     self.assertEqual(currentTitles[0], wantedTitle)
    def test_get_multiPageTitle(self):
        func = Article_crawler.get_pageTitles(self, 1)
        wantedTitle = "백남기 농민 쏜 살수차, 수압제한 장치 고장나 있었다"
        titles = Article_crawler.get_multiPageTitles(self, func)
        self.assertEqual(titles[-1], wantedTitle)


#
if __name__ == '__main__':
    unittest.main()
