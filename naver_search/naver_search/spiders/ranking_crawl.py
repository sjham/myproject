# -*- coding: utf-8 -*-
import scrapy
import datetime
#import datetime.time
from naver_search.items import NaverSearchItem
from naver_search.url_parser import UrlParser as up
from naver_search.date_parser import DateParser as dp


class RankingCrawlSpider(scrapy.Spider):
    name = "ranking_crawl"
    allowed_domains = ["news.naver.com"]
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    tmpFile = "/media/sf_share_u/crawled_text/naver_search/naversearch_%s_to_%s.csv" % (sd, ed)
    search_urls = up.getSearchUrls(dp.getTargetdate(dp.getDate(sd, ed)))
    comment_urls = up.getCommentUrls(dp.getTargetdate(dp.getDate(sd, ed)))
    comment_total_urls = up.getCommentTotalUrls(dp.getTargetdate(dp.getDate(sd, ed)))
    # print(comment_total_urls)
    click_urls = up.getClickUrls(dp.getTargetdate(dp.getDate(sd, ed)))
    # print(click_urls)
    click_total_urls = up.getClickTotalUrls(dp.getTargetdate(dp.getDate(sd, ed)))
    # print(click_total_urls)

    def start_requests(self):
        for url in RankingCrawlSpider.search_urls:
            yield scrapy.Request(url, self.search)

        for url in RankingCrawlSpider.comment_urls:
            yield scrapy.Request(url, self.comment)

        for url in RankingCrawlSpider.comment_total_urls:
            yield scrapy.Request(url, self.comment_total)

        for url in RankingCrawlSpider.click_urls:
            yield scrapy.Request(url, self.click)

        for url in RankingCrawlSpider.click_total_urls:
            yield scrapy.Request(url, self.click_total)

    def search(self, response):
        # item = NaverSearchItem()
        # item['dates'] = response.xpath('//span[@class="c_date"]/text()').extract_first()
        for sel in response.xpath('//div[@class="ranking_keyword"]/ul/li'):
            item = NaverSearchItem()
            item['dates'] = response.xpath('//span[@class="c_date"]/text()').extract_first()
            item['rank'] = sel.xpath('./span[@class="rank"]/text()').extract_first()
            item['keywords'] = sel.xpath('./div/a/text()').extract_first()
            # print(item['rank'])
            # print(item['keywords'])
            yield item


    def comment(self, response):
        for sel in response.xpath('//div[@class="content"]/div/ol/li'):
            item = NaverSearchItem()
            item['cdates'] = response.xpath('//span[@class="c_date"]/text()').extract_first()
            item['carea'] = response.xpath('//*[@class="on"]/text()').extract_first()
            absolute_url = 'http://news.naver.com/' + sel.xpath('./dl/dt/a/@href').extract_first()
            # print(absolute_url)
            request = scrapy.Request(absolute_url, callback=self.comment_page)
            request.meta['item'] = item
            item['ctitle'] = sel.xpath('./dl/dt/a/text()').extract_first()
            item['csource'] = sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()').extract()
            item['cdatestamp'] = sel.xpath('./dl/dt/span[3]/text()').extract_first()
            if not sel.xpath('./dl/dt/span[3]/text()').extract_first():
                item['cdatestamp'] = sel.xpath('./dl/dd/span[3]/text()').extract_first()
            print(item['ctitle'])
            print(item['cdatestamp'])
            yield request

    def comment_page(self, response):
        item = response.meta['item']
        if not item['csource']:
            item['csource'] = response.xpath('//*[@class="press_logo"]/a/img/@alt').extract_first()
        # print(item['csource'])
        yield item

    def comment_total(self, response):
        for sel in response.xpath('//div[@class="content"]/div/ol/li'):
            item = NaverSearchItem()
            absolute_url = 'http://news.naver.com/' + sel.xpath('./dl/dt/a/@href').extract_first()
            request = scrapy.Request(absolute_url, callback=self.comment_total_page)
            request.meta['item'] = item
            item['cttitle'] = sel.xpath('./dl/dt/a/text()').extract_first()
            item['ctsource'] = sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()').extract()
            if not sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()'):
                item['ctsource'] = sel.xpath('./dl/dd/span[1]//descendant-or-self::*/text()').extract()
            item['ctdatestamp'] = sel.xpath('./dl/dt/span[3]/text()').extract_first()
            if not sel.xpath('./dl/dt/span[3]/text()').extract_first():
                item['ctdatestamp'] = sel.xpath('./dl/dd/span[3]/text()').extract_first()
            # print(item['cttitle'])
            # print(item['ctdatestamp'])
            # print(item['ctsource'])
            yield request
    #
    def comment_total_page(self, response):
        item = response.meta['item']
        if not item['ctsource']:
            item['ctsource'] = response.xpath('//*[@class="press_logo"]/a/img/@alt').extract_first()
        item['ctarticleText'] = ' '.join(s.strip().replace("// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "") for s in response.xpath('//div[@id="articleBodyContents"]/descendant-or-self::*/text()').extract())
        yield item

    def click(self, response):
        for sel in response.xpath('//div[@class="content"]/div/ol/li'):
            item = NaverSearchItem()
            item['ldates'] = response.xpath('//span[@class="c_date"]/text()').extract_first()
            item['larea'] = response.xpath('//*[@class="on"]/text()').extract_first()
            absolute_url = 'http://news.naver.com/' + sel.xpath('./dl/dt/a/@href').extract_first()
            # print(absolute_url)
            request = scrapy.Request(absolute_url, callback=self.click_page)
            request.meta['item'] = item
            item['ltitle'] = sel.xpath('./dl/dt/a/text()').extract_first()
            item['lsource'] = sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()').extract()
            item['ldatestamp'] = sel.xpath('./dl/dt/span[3]/text()').extract_first()
            if not sel.xpath('./dl/dt/span[3]/text()').extract_first():
                item['ldatestamp'] = sel.xpath('./dl/dd/span[3]/text()').extract_first()
            # print(item['ltitle'])
            # print(item['ldatestamp'])
            yield request

    def click_page(self, response):
        item = response.meta['item']
        if not item['lsource']:
            item['lsource'] = response.xpath('//*[@class="press_logo"]/a/img/@alt').extract_first()
        # print(item['lsource'])
        yield item
    #
    def click_total(self, response):

        for sel in response.xpath('//div[@class="content"]/div/ol/li'):
            item = NaverSearchItem()
            absolute_url = 'http://news.naver.com/' + sel.xpath('./dl/dt/a/@href').extract_first()
            request = scrapy.Request(absolute_url, callback=self.click_total_page)
            request.meta['item'] = item
            item['lttitle'] = sel.xpath('./dl/dt/a/text()').extract_first()
            # item['ltsource'] = sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()').extract()
            # if not sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()'):
            #     item['ltsource'] = sel.xpath('./dl/dd/span[1]//descendant-or-self::*/text()').extract()
            item['ltdatestamp'] = sel.xpath('./dl/dt/span[3]/text()').extract_first()
            if not sel.xpath('./dl/dt/span[3]/text()').extract_first():
                item['ltdatestamp'] = sel.xpath('./dl/dd/span[3]/text()').extract_first()
            # print(item['lttitle'])
            # print(item['ltdatestamp'])
            yield request

    def click_total_page(self, response):
        item = response.meta['item']
        item['ltsource'] = response.xpath('//*[@class="press_logo"]/a/img/@alt').extract_first()
        item['ltarticleText'] = ' '.join(s.strip().replace("// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "") for s in response.xpath('//div[@id="articleBodyContents"]/descendant-or-self::*/text()').extract())
        # print(item['ltsource'])
        yield item
