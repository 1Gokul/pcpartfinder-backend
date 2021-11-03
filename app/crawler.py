from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from part_scraper.spiders.vedant_computers import VedantSpider

process = CrawlerProcess(get_project_settings())

if __name__=="__main__":
    process.crawl(VedantSpider)
    process.start()