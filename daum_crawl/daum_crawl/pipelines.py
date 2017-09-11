## -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import datetime
#import MySQLdb

class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(spider.tmpFile, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['title', 'source', 'expotime', 'articleText']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        print(datetime.datetime.now())
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# from navermobile_crawl.items import NavermobileCrawlItem
#
# class PricePipeline(object):
#     def process_item(self, item, spider):
#
#         print(item['title'])
#
# #
# class MySQLStorePipeline(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect(host='127.0.0.1', user='ham', passwd='5864', db='scrapy', charset="utf8", use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         try:
#             # self.cursor.execute("""INSERT INTO naver(title, source, expotime, expodur, articleText, link, expotime2, expotime3, expotime4, expotime5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)""", (item['title'], item['source'], item['expotime'], item['expodur'], item['articleText'].encode('utf-8'), item['link'], item['expotime2'], item['expotime3'], item['expotime4'], item['expotime5']))
#             self.cursor.execute("""INSERT INTO naver(title, source, expotime, articleText, link, expotime2, expotime3, expotime4, expotime5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (item['title'], item['source'], item['expotime'], item['articleText'].encode('utf-8'), item['link'], item['expotime2'], item['expotime3'], item['expotime4'], item['expotime5']))
#             self.conn.commit()
#         except MySQLdb.Error as e:
#             print ("Error %d: %s" % (e.args[0], e.args[1]))
#             return None
#         except IndexError:
#             print ("MySQL Error: %s" % str(e))
#             return None
#         except TypeError as e:
#             print(e)
#             return None
#         except ValueError as e:
#             print(e)
#             return None
#         return item
#
# class CsvExportPipeline(object):
#     def __init__(self):
#         self.files = {}
#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline
#
#     def spider_opened(self, spider):
#         file = open(spider.tmpFile, 'w+b')
#         self.files[spider] = file
#         self.exporter = CsvItemExporter(file)
#         self.exporter.fields_to_export = ['title', 'source', 'expotime', 'articleText', 'link', 'expotime2', 'expotime3', 'expotime4', 'expotime5']
#         self.exporter.start_exporting()
#
#     def spider_closed(self, spider):
#         self.exporter.finish_exporting()
#         file = self.files.pop(spider)
#         print(datetime.datetime.now())
#         file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         print(item)
#         return item
#
# class NavermobileCrawlPipeline(object):
#     def process_item(self, item, spider):
#         return item
