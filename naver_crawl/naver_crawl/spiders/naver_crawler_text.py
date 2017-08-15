
import scrapy
import datetime
#import datetime.time
from naver_crawl.items import NaverCrawlItem
from naver_crawl.url_parser import UrlParser as up
from naver_crawl.date_parser import DateParser as dp

class NaverCrawlerSpider(scrapy.Spider):
    print(datetime.datetime.now())
    name = "naver_crawler_text"
    allowed_domains = ["news.naver.com"]
    sd = input("Start Date(yyyy,m,d): ")
    ed = input("End Date(yyyy,m,d): ")
    tmpFile = "/home/ham/Envs/scrapy/crawled_data/navercrawl_%s_to_%s.csv" % (sd, ed)
    urls = up.getDayUrls(dp.getDate(sd, ed))

    def start_requests(self):
        for url in NaverCrawlerSpider.urls:
            for i in range(1, 15):
                real_url = url+'{}'.format(i)
                yield scrapy.Request(real_url, self.parse)

    def parse(self, response):
        for sel in response.xpath('//body/ul/li'):
            item = NaverCrawlItem()
            absolute_url = sel.xpath('./a/@href').extract_first()
            request = scrapy.Request(absolute_url, callback=self.parse_page)
            request.meta['item'] = item
            item['title'] = sel.xpath('./a/text()').extract_first()
            item['link'] = sel.xpath('./a/@href').extract_first()
            item['source'] = sel.xpath('./span/span[1]/text()').extract_first()
            item['expotime'] = sel.xpath('./span/span[3]/text()').extract_first()
            #item['expodur'] = sel.xpath('./span/span[3]/text()').extract_first().split(' ')[5]

            item['expotime2'] = sel.xpath('./span/span[5]/text()').extract_first()
            item['expotime3'] = sel.xpath('./span/span[7]/text()').extract_first()
            item['expotime4'] = sel.xpath('./span/span[9]/text()').extract_first()
            item['expotime5'] = sel.xpath('./span/span[11]/text()').extract_first()
            yield request

    def parse_page(self, response):
        item = response.meta['item']
        item['articleText'] = ' '.join(s.strip().replace("// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "") for s in response.xpath('//div[@id="articleBodyContents"]/descendant-or-self::*/text()').extract())
        print(item['articleText'])
        print(item['title'])
        yield item
