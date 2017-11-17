# -*- coding: utf-8 -*-
import scrapy
import datetime
#import datetime.time
from naver_wranking.items import NaverWrankingItem
from naver_wranking.url_parser import UrlParser as up
from naver_wranking.date_parser import DateParser as dp


class RankingCrawlSpider(scrapy.Spider):
    name = "ranking_crawl"
    allowed_domains = ["news.naver.com"]
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    tmpFile = "/media/sf_share_u/crawled_text/naver_wranking/naverwranking_%s_to_%s.csv" % (sd, ed)
    ranking_urls = up.getRankingUrls(dp.getDate(sd, ed))
    total_urls = up.getTotalUrls(dp.getDate(sd, ed))
    # print(ranking_urls)

    def start_requests(self):
        for url in RankingCrawlSpider.ranking_urls:
            yield scrapy.Request(url, self.ranking)
        for url in RankingCrawlSpider.total_urls:
            yield scrapy.Request(url, self.total)

    def ranking(self, response):
        for sel in response.xpath('//div[@class="content"]/div/ol/li'):
            # if not response.xpath('//div[@class="content"]/div/ol/li'):
            #     response.xpath('//div[@id="ranking_list"]/div/ol/li'):
            item = NaverWrankingItem()
            absolute_url = 'http://news.naver.com/' + sel.xpath('./dl/dt/a/@href').extract_first()
            print(absolute_url)
            request = scrapy.Request(absolute_url, callback=self.ranking_page)
            request.meta['item'] = item
            item['area'] = response.xpath('//*[@class="on"]/text()').extract_first()
            item['title'] = sel.xpath('./dl/dt/a/text()').extract_first()

            item['datestamp'] = sel.xpath('./dl/dt/span[3]/text()').extract_first()
            print(item['title'])
            print(item['datestamp'])
            yield request

    def ranking_page(self, response):
        item = response.meta['item']
        item['source'] = response.xpath('//*[@class="press_logo"]/a/img/@alt').extract_first()
        # item['datestamp'] = response.xpath('//*[@class="media_end_head_info_datestamp_time"]/text()').extract_first()
        # item['comment'] = response.xpath('//*[@class="u_cbox_count"]/text()').extract_first()
        print(item['source'])
        yield item

    def total(self, response):
        for sel in response.xpath('//div[@class="content"]/div/ol/li'):
            item = NaverWrankingItem()
            absolute_url = 'http://news.naver.com/' + sel.xpath('./dl/dt/a/@href').extract_first()
            request = scrapy.Request(absolute_url, callback=self.total_page)
            request.meta['item'] = item
            item['ttitle'] = sel.xpath('./dl/dt/a/text()').extract_first()
            item['tsource'] = sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()').extract()
            if not sel.xpath('./dl/dt/span[1]/descendant-or-self::*/text()'):
                item['tsource'] = sel.xpath('./dl/dd/span[1]//descendant-or-self::*/text()').extract()
            item['tdatestamp'] = sel.xpath('./dl/dt/span[3]/text()').extract_first()
            print(item['ttitle'])
            print(item['tdatestamp'])
            yield request

            # response.xpath('//div[@id="articleBodyContents"]/descendant-or-self::*/text()').extract())

    def total_page(self, response):
        item = response.meta['item']
        item['tarticleText'] = ' '.join(s.strip().replace("// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "") for s in response.xpath('//div[@id="articleBodyContents"]/descendant-or-self::*/text()').extract())

        # item['tcount'] = response.xpath('//div[@id="cbox_module"]/div/div[2]/ul/li/span/text()').extract_first()
        # item['tsource'] = response.xpath('//*[@class="press_logo"]/a/img/@alt').extract_first()
        # item['datestamp'] = response.xpath('//*[@class="media_end_head_info_datestamp_time"]/text()').extract_first()
        # item['comment'] = response.xpath('//*[@class="u_cbox_count"]/text()').extract_first()
        # response.xpath('//em[@class="u_cnt _count"]/text()').extract_first()
        print(item['tarticleText'])
        yield item
