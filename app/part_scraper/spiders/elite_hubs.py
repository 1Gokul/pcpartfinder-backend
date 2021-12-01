import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
    # "power-supply-unit-psu",
    # "pc-coolers",
    # "storage-ssd-hard-disk",
    # "monitor",
    "graphic-cards",
    # "ram",
    # "processor",
    # "gaming-keyboard",
    # "motherboard",
    # "pc-cabinet",
    # "gaming-mouse",
    # "gaming-headphone"
]


class EliteHubsSpider(scrapy.Spider):
    name = "elite_hubs"
    allowed_domains = ["elitehubs.com/"]
    start_urls = [
        f"https://elitehubs.com/{category}"
        for category in CATEGORIES
    ]

    def parse(self, response):

        items = response.css("ul#product_listing .item .item-content")
        print(items)
        for item in items:
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css("name", "h4 a::text")
            loader.add_css("price", "span.item-price span.amount bdi::text")
            loader.add_css("url", "h4 a::attr(href)")
            loader.add_value("store", "Elite_Hubs")

            yield loader.load_item()

        # for link in response.css(".ias-trigger.ias-trigger-next a"):
        #     yield response.follow(link, callback=self.parse)
