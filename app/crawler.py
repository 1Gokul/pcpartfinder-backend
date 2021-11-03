from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from part_scraper.spiders.md_computers import MDComputersSpider

from part_scraper.spiders.vedant_computers import VedantComputersSpider

process = CrawlerProcess(get_project_settings())

Spiders = [VedantComputersSpider, MDComputersSpider]

if __name__ == "__main__":
    process.crawl(VedantComputersSpider)
    process.crawl(MDComputersSpider)
    process.start()
