# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DaumCrawlItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    expotime = scrapy.Field()
    # expotime2 = scrapy.Field()
    # starttime = scrapy.Field()
    # endtime = scrapy.Field()
    # #expodur = scrapy.Field()
    articleText = scrapy.Field()
