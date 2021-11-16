import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
    # "peripherals",
    # "cabinet",
    # "smps",
    # "cooling-system",
    # "storage",
    # "monitors",
    "graphics-card",
    # "memory",
    # "processor",
    # "motherboards",
]


class MDComputersSpider(scrapy.Spider):
    name = "md_computers"
    allowed_domains = ["mdcomputers.in"]
    start_urls = [f"https://mdcomputers.in/{category}" for category in CATEGORIES]

    def parse(self, response):

        items = response.css(".products-list .product-item-container")

        for item in items:
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

        
        # Goes to the next page using the pagination links at the bottom
        next_page_url = response.css(".pagination > li:nth-last-child(2) > a::attr(href)").get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

