from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

SPIDERS = [
    "Vedant_Computers",
    "MD_Computers",
    "Prime_ABGB",
    "IT_Depot",
    "PC_Shop",
    "PC_Studio",
    "Elite_Hubs",
    "National_PC",
]

if __name__ == "__main__":
    for spider in SPIDERS:
        process.crawl(spider.lower())
    process.start()
