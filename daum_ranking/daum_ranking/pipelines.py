from scrapy import signals
from scrapy.exporters import CsvItemExporter
import datetime

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
        self.exporter.fields_to_export = ['title', 'rank', 'area', 'source', 'datestamp', 'ctitle', 'crank', 'ccomment', 'carea', 'csource', 'cdatestamp']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        print(datetime.datetime.now())
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
