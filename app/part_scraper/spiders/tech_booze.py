import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem
from config import DB_CATEGORIES

SITE_CATEGORIES = [
    # "peripherals",
    # "cabinets",
    # "psu",
    # "cooling-solution",
    # "storage",
    # "gaming-monitors",
    "graphics-cards",
    # "ram",
    # "amd-cpu",
    # "motherboards",
    # "networking",
]


class TechBoozeSpider(scrapy.Spider):
    name = "tech_booze"
    allowed_domains = ["techbooze.in"]
    start_urls = [
        f"https://www.techbooze.in/{category}/?stock_status=instock"
        for category in SITE_CATEGORIES
    ]

    def parse(self, response):

        items = response.css(".products.elements-grid .product-grid-item")

        # Get the current category of the items. It will be needed for the "category"
        # column in the database.
        category = DB_CATEGORIES[response.request.url.split("/")[3]]

        for item in items:
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css(
                "name", "div.product-information h3.wd-entities-title a::text"
            )
            loader.add_css(
                "price",
                "div.product-information div.product-rating-price span.amount bdi::text",
            )
            loader.add_css(
                "url", "div.product-information h3.wd-entities-title a::attr(href)"
            )
            loader.add_value("category", category)
            loader.add_value("store", "Tech_Booze")

            yield loader.load_item()

        # Goes to the next page using the pagination links at the bottom
        next_page_url = response.css(
            "ul.page-numbers > li:nth-last-child(1) > a::attr(href)"
        ).get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
