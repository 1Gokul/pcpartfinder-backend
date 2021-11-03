import scrapy
from scrapy import selector
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

urls = [
    "peripherals",
    "cabinet",
    "smps",
    "cooling-system",
    "storage",
    "monitors",
    "graphics-card",
    "memory",
    "processor",
    "motherboards",
]


class MDComputersSpider(scrapy.Spider):
    name = "md_computers"
    allowed_domains = ["mdcomputers.in/"]
    start_urls = [f"https://mdcomputers.in/{url}" for url in urls]

    def parse(self, response):

        items = response.css(".products-list .product-item-container")

        for item in items:
            print(item)
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css(
                "name", "div.product-item-container div.right-block h4 a::text"
            )
            loader.add_css(
                "price",
                "div.product-item-container div.right-block div.price span.price-new::text",
            )
            loader.add_css(
                "url", "div.product-item-container div.right-block h4 a::attr(href)"
            )
            loader.add_value("store", "MD_Computers")

            yield loader.load_item()
