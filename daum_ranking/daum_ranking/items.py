# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#
#
# def serialize_rank(value):
#     return 'Nr {}'.format(value)


class DaumRankingItem(scrapy.Item):
    title = scrapy.Field()
    # rank = scrapy.Field(serializer=serialize_rank)
    rank = scrapy.Field()
    area = scrapy.Field()
    source = scrapy.Field()
    datestamp = scrapy.Field()

    ctitle = scrapy.Field()
    crank = scrapy.Field()
    ccomment = scrapy.Field()
    carea = scrapy.Field()
    csource = scrapy.Field()
    cdatestamp = scrapy.Field()

    # ktitle = scrapy.Field()
    # krank = scrapy.Field()
    # karea = scrapy.Field()
    # ksource = scrapy.Field()
    # kdatestamp = scrapy.Field()
    # print(title)
