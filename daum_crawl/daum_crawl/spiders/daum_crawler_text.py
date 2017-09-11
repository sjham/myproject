# -*- coding: utf-8 -*-
import scrapy
import datetime
from daum_crawl.items import DaumCrawlItem
from daum_crawl.date_parser import DateParser as dp

class DaumCrawlerTextSpider(scrapy.Spider):
    print(datetime.datetime.now())
    name = "daum_crawler_text"
    allowed_domains = ["media.daum.net"]
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    tmpFile = "/media/sf_share_u/crawled_text/daumcrawl_%s_to_%s.csv" % (sd, ed)
    datesSet = dp.getDate(sd, ed)

    def start_requests(self):
        for dates in self.datesSet:
            for i in range(1, 20):
                real_url = 'http://media.daum.net/newsbox?page={}&tab_cate=NE&regDate={}'.format(i, dates.replace('-', ''))
                #print(real_url)
                yield scrapy.Request(real_url, self.parse)

    def parse(self, response):
        for sel in response.xpath('//*[@id="mArticle"]/div[3]/ul/li'):
            item = DaumCrawlItem()
            absolute_url = sel.xpath('./a/@href').extract_first()
            request = scrapy.Request(absolute_url, callback=self.parse_page)
            request.meta['item'] = item
            item['title'] = sel.xpath('./a/text()').extract_first()
            #print(item['title'])
            yield request

    def parse_page(self, response):
        item = response.meta['item']
        item['source'] = response.xpath('//*[@id="cSub"]/div[1]/em/a/img/@*')[0].extract()
        item['expotime'] = response.xpath('//*[@id="cSub"]/div[1]/span/span[@class="txt_info"]/text()').extract()
        item['articleText'] = ' '.join(s.strip() for s in response.xpath('//div[@id="harmonyContainer"]/descendant-or-self::*/text()').extract())
        print(item['articleText'])
        print(item['title'])
        yield item
