import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
    # "motherboards",
    # "it-peripheral",
    # "speakers",
    # "memory",
    # "computer-case",
    # "power-supply",
    # "fans-coolings",
    # "processor",
    # "storage",
    # "gaming-monitors",
    "graphic-card",
]


class PCShopSpider(scrapy.Spider):
    name = "pc_shop"
    allowed_domains = ["pcshop.in"]
    start_urls = [f"https://www.pcshop.in/product-category/{category}/" for category in CATEGORIES]

    def parse(self, response):

        items = response.css(".products .product-item__inner")

        for item in items:
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css(
                "name", "div.product-item__header h2.woocommerce-loop-product__title::text"
            )
            loader.add_css(
                "price",
                "div.product-item__footer span.woocommerce-Price-amount bdi::text",
            )
            loader.add_css(
                "url", "div.product-item__header a.woocommerce-loop-product__link::attr(href)"
            )
            loader.add_value("store", "PC_Shop")

            yield loader.load_item()

        
        # Goes to the next page using the pagination links at the bottom
        next_page_url = response.css(".electro-advanced-pagination a.next.page-numbers::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

