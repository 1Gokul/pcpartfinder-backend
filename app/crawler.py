from scrapy.crawler import CrawlerProcess

from part_scraper.spiders.vedant import VedantSpider


process = CrawlerProcess()

if __name__=="__main__":
    process.crawl(VedantSpider)
    process.start()