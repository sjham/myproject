
import unittest

from article import Article_crawler
from input_value import InputValue

class Article_crawlerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_getDatesSet_success(self):
        inputValue = InputValue("2017,6,25", "2017,6,27")
        datesSet = Article_crawler.getDatesSet(inputValue)
        self.assertEqual(datesSet, ['2017-06-25', '2017-06-26', '2017-06-27'])

    def test_getDatesSet_fail(self):
        inputValue = InputValue("2017,6,27", "2017,6,25")
        datesSet = Article_crawler.getDatesSet(inputValue)
        self.assertEqual(datesSet, ["2017-06-25", "2017-06-26", "2017-06-27"])


    def test_getHtml(self):
        pass


if __name__ == '__main__':
    unittest.main()
