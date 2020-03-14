#!/usr/bin/python3
# -*- coding: utf-8 -*-


import scrapy
import sys
import os

from scrapy.http import Request, FormRequest
from datascraper.items import DataItem, convertToInt, convertToFloat
import time
import datetime

import logging
import re
import json
import math
from hashlib import md5
import csv


from scrapy.loader import ItemLoader
from scrapy.utils.response import open_in_browser


logger = logging.getLogger(__name__)


def readCSV_to_list(filePath):
    ''' Read csv file to list'''
    if not os.path.isfile(filePath):
        logger.debug('File %s not found', filePath)
        return []
    with open(filePath, 'r', encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        return list(reader)

class Etuannv(scrapy.Spider):
    name = "cik_spd"

    # Config table name
    generalproduct = 'generalproduct'

    # Config custom setting
    custom_settings = {
        'IS_STOP_REPORT': False,
        'MYSQL_TABLE': generalproduct,
        # 'DOWNLOAD_TIMEOUT'   : 180,
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 5,
        'RETRY_TIMES': 5,
        'HTTPERROR_ALLOWED_CODES': [],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 543,
            'datascraper.middlewares.MySpiderMiddleware': 100,
            'datascraper.middlewares.RandomUserAgentMiddleware': 400,
            # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':543,
        },
        # 'ROTATING_PROXY_BAN_POLICY':'datascraper.middlewares.MyDetectionPolicy',
        'ITEM_PIPELINES': {
            'datascraper.pipelines.CsvPipeline': 100,
            # 'datascraper.pipelines.MySQLPipeline': 200,
        },
    }

    # === Init function ===
    def __init__(self, scraped_key=None, *args, **kwargs):
        super(Etuannv, self).__init__(*args, **kwargs)
        if scraped_key is not None:
            self.scraped_key = scraped_key
        else:
            # Random key
            self.scraped_key = self.name + '_' + datetime.datetime.now().strftime("%Y%m%d")

    # === start request to scrape data ===

    def start_requests(self):
        """Start request data.
        """
        urls = readCSV_to_list('url list.csv')
        self.crawler.stats.set_value('total', len(urls))
        for row in urls:
            
            if row[0].endswith(".xml"):
                yield Request(
                    row[0],
                    callback=self.parse
                )
        
    

    def parse(self, response):
        data_item = ItemLoader(item=DataItem(), response=response)
        data_item.add_value('url', response.url)

        # Parse arccurate
        accurates = re.findall(r'AccruedEnvironmentalLossContingenciesCurrent contextRef="(.[^"]*).*">(\d+)', response.text)
        if accurates:
            for a in accurates:
                item = '{}:{}'.format(a[0], a[1])
                data_item.add_value('accurate', item)
        
        # Parse cik code
        ciks = re.findall(r'CIK">(\d+)', response.text)
        
        item_list = []
        if ciks:
            for a in ciks:
                if a not in item_list:
                    item_list.append(a)
        data_item.add_value('cik', item_list)

        self.crawler.stats.inc_value('done')
        yield data_item.load_item()
