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

PRODUCTS_LIMIT = 100


class NationalPCSpider(scrapy.Spider):
    name = "national_pc"
    allowed_domains = ["nationalpc.in"]
    start_urls = [
        f"https://nationalpc.in/computer-hardware/computer-components/{category}/in-stock/limit-{PRODUCTS_LIMIT}?"
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

            # Scraping next pages
            # Check if the "page_no" variable exists.
            # If it doesn't exist, we are on the first page and we thus assign it the value 2.
            page_no = response.meta.get("page_no")
            page_no = int(page_no) + 1 if page_no else 2

            # Remove the part of the url that has the previous page number and append the new one.
            next_page_url = f"{response.request.url.rpartition('?')[0]}?page={page_no}"
            if next_page_url:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(
                    url=next_page_url, callback=self.parse, meta={"page_no": page_no}
                )
