import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
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

PRODUCTS_LIMIT = 999


class VedantComputersSpider(scrapy.Spider):
    name = "vedant_comptuers"
    allowed_domains = ["vedantcomputers.com/pc-components/"]
    start_urls = [
        f"https://www.vedantcomputers.com/pc-components/{category}?limit={PRODUCTS_LIMIT}"
        for category in CATEGORIES
    ]

    def parse(self, response):

        items = response.css(".main-products.product-grid .caption")

        for item in items:
            # VedantComputers adds the "limit" argument to all the links in the search results for some reason.
            # This strips them from the link.
            url = (
                item.css("div.name a::attr(href)")
                .get()
                .replace(f"&limit={PRODUCTS_LIMIT}", "")
                .replace(f"?limit={PRODUCTS_LIMIT}", "")
            )

            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css("name", "div.name a::text")
            loader.add_css("price", ".price-normal::text")
            loader.add_value("url", url)
            loader.add_value("store", "Vedant_Computers")

            yield loader.load_item()

        # for link in response.css(".ias-trigger.ias-trigger-next a"):
        #     yield response.follow(link, callback=self.parse)
