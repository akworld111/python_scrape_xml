# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
MIT License

scrapy_mysql_pipeline: Asynchronous mysql Scrapy item pipeline

Copyright (c) 2017 Iaroslav Russkykh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Requirements:
- scrapy>=1.4.0
- pymysql>=0.7.11

"""

import logging
import pprint
from scrapy.exceptions import DropItem
import os
from scrapy.exporters import CsvItemExporter

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')



class CsvPipeline(object):  #
    
    stats_name = 'csvpipeline'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.stats.set_value('done', 0)
        self.settings = crawler.settings
        
    def open_spider(self, spider):
        if not os.path.exists(spider.scraped_key):
            os.makedirs(spider.scraped_key)
        
        self.file = open(f'{spider.scraped_key}_result.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        print('\n\n')
        
        logger.info(f'===> RESULT AT:{spider.scraped_key}_result.csv')


    # @defer.inlineCallbacks
    def process_item(self, item, spider):
        self.stats.inc_value('done')
        self.exporter.export_item(item)
        if self.stats.get_value('done') % 100 == 0:
            logger.info("--> CSV pineline: Done %s/ %s", self.stats.get_value('done'), self.stats.get_value('total'))
        
        return item
        
        
