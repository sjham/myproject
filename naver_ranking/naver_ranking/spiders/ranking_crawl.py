# -*- coding: utf-8 -*-
import scrapy
import datetime
#import datetime.time
from naver_ranking.items import NaverRankingItem
from naver_ranking.url_parser import UrlParser as up
from naver_ranking.date_parser import DateParser as dp

class RankingCrawlSpider(scrapy.Spider):
    name = "ranking_crawl"
    allowed_domains = ["m.news.naver.com"]
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    tmpFile = "/media/sf_share_u/crawled_text/naverranking/naverranking_%s_to_%s.csv" % (sd, ed)
    ranking_urls = up.getRankingUrls(dp.getDate(sd, ed))
    comment_urls = up.getCommentUrls(dp.getDate(sd, ed))
    print(ranking_urls)

    def start_requests(self):
        for url in RankingCrawlSpider.ranking_urls:
            yield scrapy.Request(url, self.ranking)
        for url in RankingCrawlSpider.comment_urls:
            yield scrapy.Request(url, self.comment)

    def ranking(self, response):
        for sel in response.xpath('//ul[@class="commonlist"]/li'):
            item = NaverRankingItem()
            absolute_url = 'http://m.news.naver.com/' + sel.xpath('./a/@href').extract_first()
            request = scrapy.Request(absolute_url, callback=self.ranking_page)
            request.meta['item'] = item
            item['area'] = sel.xpath('//*[@class="h2_area_inner"]/h2/text()').extract_first()
            item['title'] = sel.xpath('./a/div[1]/div[1]/text()').extract_first()
            item['visit'] = sel.xpath('./a/div[1]/div[2]/text()').extract_first()
            yield request

    def ranking_page(self, response):
        item = response.meta['item']
        item['source'] = response.xpath('//*[@class="media_end_head_top"]/a/img/@alt').extract_first()
        item['datestamp'] = response.xpath('//*[@class="media_end_head_info_datestamp_time"]/text()').extract_first()
        print(item['title'])
        yield item

    def comment(self, response):
        for sel in response.xpath('//ul[@class="commonlist"]/li'):
            item = NaverRankingItem()
            absolute_url = 'http://m.news.naver.com/' + sel.xpath('./a/@href').extract_first()
            print(absolute_url)
            request = scrapy.Request(absolute_url, callback=self.comment_page)
            request.meta['item'] = item
            item['carea'] = sel.xpath('//*[@class="h2_area_inner"]/h2/text()').extract_first()
            item['ctitle'] = sel.xpath('./a/div[1]/div[1]/text()').extract_first()
            item['ccount'] = sel.xpath('./a/div[1]/div[2]/text()').extract_first()
            # print(item['ctitle'])
            yield request

    def comment_page(self, response):
        item = response.meta['item']
        item['csource'] = response.xpath('//*[@class="media_end_head_top"]/a/img/@alt').extract_first()
        item['cdatestamp'] = response.xpath('//*[@class="media_end_head_info_datestamp_time"]/text()').extract_first()
        yield item
