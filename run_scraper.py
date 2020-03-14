from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from datascraper.spiders.cikspider import Etuannv
import datetime
from scrapy.utils.project import get_project_settings


configure_logging()
config = get_project_settings()
# config['FEED_URI'] = 'output_file.csv'
# config['FEED_FORMAT'] = 'csv'
runner = CrawlerRunner(settings=config)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(Etuannv)
    reactor.stop()
    

crawl()
reactor.run() # the script will block here until the last crawl call is finished