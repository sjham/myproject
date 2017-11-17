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


class NaverSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rank = scrapy.Field()
    keywords = scrapy.Field()
    dates = scrapy.Field()

    carea = scrapy.Field()
    cdates = scrapy.Field()
    ctitle = scrapy.Field()
    csource = scrapy.Field(serializer=serialize_line)
    cdatestamp = scrapy.Field()

    ccomment = scrapy.Field()
    cttitle = scrapy.Field()
    ctsource = scrapy.Field(serializer=serialize_line)
    ctdatestamp = scrapy.Field()
    ctarea = scrapy.Field()
    ctarticleText = scrapy.Field()

    larea = scrapy.Field()
    ldates = scrapy.Field()
    ltitle = scrapy.Field()
    lsource = scrapy.Field(serializer=serialize_line)
    ldatestamp = scrapy.Field()

    lttitle = scrapy.Field()
    ltdatestamp = scrapy.Field()
    ltsource = scrapy.Field(serializer=serialize_line)
    ltarticleText = scrapy.Field()
