
import scrapy

class NaverCrawlItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    category = scrapy.Field()
    expotime = scrapy.Field()
    articleText = scrapy.Field()
    link = scrapy.Field()
    expotime2 = scrapy.Field()
    expotime3 = scrapy.Field()
    expotime4 = scrapy.Field()
    expotime5 = scrapy.Field()
