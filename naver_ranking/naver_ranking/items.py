# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NaverRankingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    visit = scrapy.Field()
    source = scrapy.Field()
    area = scrapy.Field()

    # hits = scrapy.Field()
    datestamp = scrapy.Field()
    comment = scrapy.Field()

    ctitle = scrapy.Field()
    ccount = scrapy.Field()
    csource = scrapy.Field()
    carea = scrapy.Field()

    # hits = scrapy.Field()
    cdatestamp = scrapy.Field()
    comment = scrapy.Field()
