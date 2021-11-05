from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from part_scraper.spiders.vedant_computers import VedantComputersSpider
from part_scraper.spiders.md_computers import MDComputersSpider
from part_scraper.spiders.the_it_depot import ITDepotSpider
from part_scraper.spiders.prime_abgb import PrimeABGBSpider


process = CrawlerProcess(get_project_settings())

Spiders = [VedantComputersSpider, MDComputersSpider, PrimeABGBSpider, ITDepotSpider]

if __name__ == "__main__":
    process.crawl(VedantComputersSpider)
    process.crawl(MDComputersSpider)
    process.crawl(PrimeABGBSpider)
    process.crawl(ITDepotSpider)
    process.start()
