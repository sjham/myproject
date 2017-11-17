# -*- coding: utf-8 -*-
import scrapy
# import datetime
#import datetime.time
from daum_ranking.items import DaumRankingItem
from daum_ranking.url_parser import UrlParser as up
from daum_ranking.date_parser import DateParser as dp


class RankingCrawlSpider(scrapy.Spider):
    name = "ranking_crawl"
    allowed_domains = ["media.daum.net"]
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    tmpFile = "/media/sf_share_u/crawled_text/daumranking/daumranking_%s_to_%s.csv" % (sd, ed)
    ranking_urls = up.getRankingUrls(dp.getDate(sd, ed))
    # kkom_urls = up.getRankingUrls(dp.getDate(sd, ed))
    comment_urls = up.getCommentUrls(dp.getDate(sd, ed))
    print(ranking_urls)
    # print(comment_urls)

    def start_requests(self):
        for url in RankingCrawlSpider.ranking_urls:
            yield scrapy.Request(url, self.ranking)
        # for url in RankingCrawlSpider.kkom_urls:
        #     yield scrapy.Request(url, self.kkom)
        for url in RankingCrawlSpider.comment_urls:
            yield scrapy.Request(url, self.comment)

    def ranking(self, response):
        for sel in response.xpath('//ul[@class="list_news2"]/li'):
            item = DaumRankingItem()
            absolute_url = sel.xpath('./div/strong/a/@href').extract_first()
            print(absolute_url)
            request = scrapy.Request(absolute_url, callback=self.ranking_page)
            request.meta['item'] = item
            item['title'] = sel.xpath('./div/strong/a/text()').extract_first()
            item['source'] = sel.xpath('./div/strong/span/text()').extract_first()
            item['rank'] = sel.xpath('./div/span/span/span/text()').extract_first()
            print(item['title'])
            print(item['rank'])
            yield request

    def ranking_page(self, response):
        item = response.meta['item']
        item['area'] = response.xpath('//*[@class="inner_gnb"]/ul/@data-category').extract_first()
        if not response.xpath('//*[@class="inner_gnb"]/ul/@data-category'):
            item['area'] = response.xpath('//*[@class="inner_gnb"]/ul/@class').extract_first()
        item['datestamp'] = response.xpath('//*[@id="cSub"]/div/span/span[2]/text()').extract_first()
        if not response.xpath('//*[@id="cSub"]/div/span/span[2]/text()'):
            item['datestamp'] = response.xpath('//*[@id="cSub"]/div[1]/span/span/text()').extract_first()
        print(item['area'])
        print(item['datestamp'])
        yield item

    def comment(self, response):
        for sel in response.xpath('//ul[@class="list_news2"]/li'):
            item = DaumRankingItem()
            absolute_url = sel.xpath('./div/strong/a/@href').extract_first()
            print(absolute_url)
            request = scrapy.Request(absolute_url, callback=self.comment_page)
            request.meta['item'] = item
            item['ctitle'] = sel.xpath('./div/strong/a/text()').extract_first()
            item['csource'] = sel.xpath('./div/strong/span/text()').extract_first()
            item['crank'] = sel.xpath('./div/span/span/span/text()').extract_first()
            item['ccomment'] = sel.xpath('./div/span[2]/span[2]/text()').extract_first()
            print(item['ctitle'])
            print(item['crank'])
            yield request
            # print(item['ctitle'])
            # print(item['crank'])
            # print(item['ccomment'])

    def comment_page(self, response):
        item = response.meta['item']
        item['carea'] = response.xpath('//*[@class="inner_gnb"]/ul/@data-category').extract_first()
        if not response.xpath('//*[@class="inner_gnb"]/ul/@data-category'):
            item['carea'] = response.xpath('//*[@class="inner_gnb"]/ul/@class').extract_first()
        item['cdatestamp'] = response.xpath('//*[@id="cSub"]/div/span/span[2]/text()').extract_first()
        if not response.xpath('//*[@id="cSub"]/div/span/span[2]/text()'):
            item['cdatestamp'] = response.xpath('//*[@id="cSub"]/div[1]/span/span/text()').extract_first()
        print(item['carea'])
        print(item['cdatestamp'])
        yield item

    #
    # def kkom(self, response):
    #     for sel in response.xpath('//ul[@class="list_news2"]/li'):
    #         item = DaumRankingItem()
    #         absolute_url = sel.xpath('./strong/a/@href').extract_first()
    #         print(absolute_url)
    #         request = scrapy.Request(absolute_url, callback=self.kkom_page)
    #         request.meta['item'] = item
    #         item['ktitle'] = sel.xpath('./div/strong/a/text()').extract_first()
    #         item['ksource'] = sel.xpath('./div/strong/span/text()').extract_first()
    #         item['krank'] = sel.xpath('./div/span/span/span/text()').extract_first()
    #         print(item['ktitle'])
    #         print(item['krank'])
    #         yield request
    #         # print(item['ctitle'])
    #         # print(item['crank'])
    #         # print(item['ccomment'])
    #
    # def kkom_page(self, response):
    #     item = response.meta['item']
    #     item['karea'] = response.xpath('//*[@class="inner_gnb"]/ul/@data-category').extract_first()
    #     if not response.xpath('//*[@class="inner_gnb"]/ul/@data-category'):
    #         item['karea'] = response.xpath('//*[@class="inner_gnb"]/ul/@class').extract_first()
    #     item['kdatestamp'] = response.xpath('//*[@id="cSub"]/div/span/span[2]/text()').extract_first()
    #     if not response.xpath('//*[@id="cSub"]/div/span/span[2]/text()'):
    #         item['kdatestamp'] = response.xpath('//*[@id="cSub"]/div[1]/span/span/text()').extract_first()
    #     print(item['karea'])
    #     print(item['kdatestamp'])
    #     yield item
    #
    #
    #

    # def kkom(self, response):
    #     for sel in response.xpath('//ul[@class="list_news rank_type1"]/li'):
    #     # for sel in response.xpath('//*[@id="kakaoContent"]/div[1]/ul[2]/li'):
    #         item = DaumRankingItem()
    #         absolute_url = 'http://m.news.naver.com/' + sel.xpath('./a/@href').extract_first()
    #         request = scrapy.Request(absolute_url, callback=self.comment_page)
    #         request.meta['item'] = item
    #         item['carea'] = sel.xpath('//*[@class="h2_area_inner"]/h2/text()').extract_first()
    #         item['ctitle'] = sel.xpath('./a/div[1]/div[1]/text()').extract_first()
    #         item['ccount'] = sel.xpath('./a/div[1]/div[2]/text()').extract_first()
    #         print(item['ctitle'])
    #         yield request
    #
    # def kkom_page(self, response):
    #     item = response.meta['item']
    #     item['csource'] = response.xpath('//*[@class="media_end_head_top"]/a/img/@alt').extract_first()
    #     item['cdatestamp'] = response.xpath('//*[@class="media_end_head_info_datestamp_time"]/text()').extract_first()
    #     yield item


    # Mobile


    # def ranking(self, response):
    #     for sel in response.xpath('//ul[@class="list_news rank_type1"]/li'):
    #         item = DaumRankingItem()
    #         absolute_url = sel.xpath('./a/@href').extract_first()
    #         print(absolute_url)
    #         request = scrapy.Request(absolute_url, callback=self.ranking_page)
    #         request.meta['item'] = item
    #         item['title'] = sel.xpath('./a/div/strong/text()').extract_first()
    #         item['rank'] = sel.xpath('./a/div[2]/span/span[1]/text()').extract_first()
    #         if not sel.xpath('./a/div[2]/span/span[1]/text()').extract_first():
    #             item['rank'] = sel.xpath('./a/div/span/span[1]/text()').extract_first()
    #         # print(item['title'])
    #         # print(item['rank'])
    #         yield request
    #
    # def ranking_page(self, response):
    #     item = response.meta['item']
    #     # item['area'] = response.xpath('//*[@class="link_viewnews #title_section"]/text()').extract_first()
    #     item['area'] = response.xpath('//*[@class="wrap_tit"]/a/text()').extract_first()
    #     item['source'] = response.xpath('//*[@class="link_cp #body #cplogo"]/img/@alt').extract_first()
    #     item['datestamp'] = response.xpath('//div[@class="info_view"]/span[2]/text()').extract_first()
    #     print(item['area'])
    #     yield item
    #
    # def comment(self, response):
    #     for sel in response.xpath('//ul[@class="list_news rank_type2"]/li'):
    #         item = DaumRankingItem()
    #         absolute_url = sel.xpath('./a/@href').extract_first()
    #         request = scrapy.Request(absolute_url, callback=self.comment_page)
    #         request.meta['item'] = item
    #         item['ctitle'] = sel.xpath('./a/div/strong/text()').extract_first()
    #         item['crank'] = sel.xpath('./a/div[2]/span[1]/span[1]/text()').extract_first()
    #         if not sel.xpath('./a/div[2]/span[1]/span[1]/text()').extract_first():
    #             item['crank'] = sel.xpath('./a/div/span[1]/span[1]/text()').extract_first()
    #         item['ccomment'] = sel.xpath('./a/div[2]/span[2]/text()').extract_first()
    #         if not sel.xpath('./a/div[2]/span[2]/text()').extract_first():
    #             item['ccomment'] = sel.xpath('./a/div/span[2]/text()').extract_first()
    #         # print(item['ctitle'])
    #         # print(item['crank'])
    #         # print(item['ccomment'])
    #         yield request
    #
    # def comment_page(self, response):
    #     item = response.meta['item']
    #     item['carea'] = response.xpath('//*[@class="wrap_tit"]/a/text()').extract_first()
    #     item['csource'] = response.xpath('//*[@class="link_cp #body #cplogo"]/img/@alt').extract_first()
    #     item['cdatestamp'] = response.xpath('//div[@class="info_view"]/span[2]/text()').extract_first()
    #     #print(item['carea'])
    #     yield item
    #

    # def kkom(self, response):
    #     for sel in response.xpath('//ul[@class="list_news rank_type1"]/li'):
    #     # for sel in response.xpath('//*[@id="kakaoContent"]/div[1]/ul[2]/li'):
    #         item = DaumRankingItem()
    #         absolute_url = 'http://m.news.naver.com/' + sel.xpath('./a/@href').extract_first()
    #         request = scrapy.Request(absolute_url, callback=self.comment_page)
    #         request.meta['item'] = item
    #         item['carea'] = sel.xpath('//*[@class="h2_area_inner"]/h2/text()').extract_first()
    #         item['ctitle'] = sel.xpath('./a/div[1]/div[1]/text()').extract_first()
    #         item['ccount'] = sel.xpath('./a/div[1]/div[2]/text()').extract_first()
    #         print(item['ctitle'])
    #         yield request
    #
    # def kkom_page(self, response):
    #     item = response.meta['item']
    #     item['csource'] = response.xpath('//*[@class="media_end_head_top"]/a/img/@alt').extract_first()
    #     item['cdatestamp'] = response.xpath('//*[@class="media_end_head_info_datestamp_time"]/text()').extract_first()
    #     yield item
