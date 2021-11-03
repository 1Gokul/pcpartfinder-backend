import scrapy
from scrapy import selector
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

urls = [
    "peripherals",
    "networking",
    "power-supply",
    "fans-and-cooling",
    "storage",
    "monitor",
    "graphics-card",
    "memory",
    "processor",
]


class VedantSpider(scrapy.Spider):
    name = "vedant"
    allowed_domains = ["vedantcomputers.com/pc-components/"]
    start_urls = [
        f"https://www.vedantcomputers.com/pc-components/{url}?limit=999" for url in urls
    ]

    def parse(self, response):

        items = response.css(".main-products.product-grid .caption")

        for item in items:
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css("name", "div.name a::text")
            loader.add_css("price", ".price-normal::text")
            loader.add_css("url", "div.name a::attr(href)")
            loader.add_value("store", "VedantComputers")

            yield loader.load_item()

        for link in response.css(".ias-trigger.ias-trigger-next a"):
            yield response.follow(link, callback=self.parse)
