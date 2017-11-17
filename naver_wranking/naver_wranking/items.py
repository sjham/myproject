# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#
def serialize_line(value):
    a = "".join(value)
    return a.replace("동영상기사", "").strip()


class NaverWrankingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area = scrapy.Field()
    title = scrapy.Field()
    visit = scrapy.Field()
    source = scrapy.Field()
    datestamp = scrapy.Field()
    comment = scrapy.Field()
    ttitle = scrapy.Field()
    # tsource = scrapy.Field()
    tsource = scrapy.Field(serializer=serialize_line)
    tdatestamp = scrapy.Field()
    tcount = scrapy.Field()
    tarea = scrapy.Field()
    tarticleText = scrapy.Field()
    # tsource = scrapy.Field()
    # tdatestamp = scrapy.Field()
