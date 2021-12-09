import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

SITE_CATEGORIES = [
    # "peripherals",
    # "computer-cases",
    # "power-supply-units",
    # "fans-and-cooling",
    # "solid-state-drives",
    # "monitors",
    "graphics-cards",
    # "rams",
    # "processors",
    # "motherboards",
    # "keyboards-and-mouse",
]


class NationalPCSpider(scrapy.Spider):
    name = "national_pc"
    allowed_domains = ["nationalpc.in"]
    start_urls = [
        f"https://nationalpc.in/computer-hardware/computer-components/{category}/limit-999"
        for category in SITE_CATEGORIES
    ]

    def parse(self, response):

        items = response.css(".product-grid .product-layout")

        for item in items:
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css("name", "div.caption div.name a::text")
            loader.add_css(
                "price",
                "div.caption div.price div span::text",
            )
            loader.add_css("url", "div.caption div.name a::attr(href)")
            loader.add_value("store", "National_PC")

            yield loader.load_item()

        # # Goes to the next page using the pagination links at the bottom
        # next_page_url = response.css(".pagination > li:nth-last-child(2) > a::attr(href)").get()
        # if next_page_url:
        #     next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)
