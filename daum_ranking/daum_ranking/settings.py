# -*- coding: utf-8 -*-
import logging

BOT_NAME = 'daum_ranking'

SPIDER_MODULES = ['daum_ranking.spiders']
NEWSPIDER_MODULE = 'daum_ranking.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'daum_ranking.pipelines.CsvExportPipeline': 300
}

LOG_FILE = 'logfile.log'
LOG_LEVEL = logging.INFO
