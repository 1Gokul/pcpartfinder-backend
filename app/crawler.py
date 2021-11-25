from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from part_scraper.spiders.vedant_computers import VedantComputersSpider
from part_scraper.spiders.md_computers import MDComputersSpider
from part_scraper.spiders.the_it_depot import ITDepotSpider
from part_scraper.spiders.prime_abgb import PrimeABGBSpider
from part_scraper.spiders.pc_studio import PCStudioSpider
from part_scraper.spiders.pc_shop import PCShopSpider


process = CrawlerProcess(get_project_settings())

SPIDERS = [VedantComputersSpider, MDComputersSpider, PrimeABGBSpider, ITDepotSpider, PCShopSpider, PCStudioSpider]

if __name__ == "__main__":
    for spider in SPIDERS:
        process.crawl(spider)
    process.start()
