from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from config import STORES

process = CrawlerProcess(get_project_settings())

if __name__ == "__main__":
    for spider in STORES:
        process.crawl(spider.lower())
    process.start()
