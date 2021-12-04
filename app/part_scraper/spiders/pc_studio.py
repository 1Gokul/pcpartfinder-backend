import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
    # ["accessories", 168],
    # ["cabinet-fan", 148],
    # ["cabinets", 73],
    # ["cooler", 147],
    ["graphics-card", 48],
    # ["motherboard", 18],
    # ["monitor", 211],
    # ["power-supply", 53],
    # ["processor", 113],
    # ["monitor", 211],
    # ["storage", 259],
]


class PCStudioSpider(scrapy.Spider):
    name = "pc_studio"
    allowed_domains = ["pcstudio.in"]
    start_urls = [
        f"https://www.pcstudio.in/product-category/{category[0]}/?jsf=woocommerce-archive&tax=product_cat:{category[1]}&pagenum=1"
        for category in CATEGORIES
    ]

    def parse(self, response):

        items = response.css(".jet-woo-products-wrapper .jet-woo-builder-product")

        for item in items:

            # Add the item only if the "out-of-stock" section does not exist.
            if not item.css("p.out-of-stock").get():
                loader = ItemLoader(item=PartScraperItem(), selector=item)
                loader.add_css(
                    "name", "h3.jet-woo-builder-archive-product-title a::text"
                )
                loader.add_css(
                    "price",
                    "div.jet-woo-builder-archive-product-price span.woocommerce-Price-amount bdi::text",
                )
                loader.add_css(
                    "url", "h3.jet-woo-builder-archive-product-title a::attr(href)"
                )
                loader.add_value("store", "PC_Studio")

                yield loader.load_item()

        """ 
        The pagination section in pcstudio.in loads too late for Scrapy to pick it up.
        So for this site, we check the amount of items on the page and keep crawling by incrementing the 
        "current_page_number" in the metadata until there are no items found.
        The only problem is that this method gpes to an extra page every time.
        I'll try to find better methods. 
        This works for now. ¯\_(ツ)_/¯
        """
        if len(items) > 0:
            next_page_number = response.meta.get("current_page_number")
            next_page_number = next_page_number + 1 if next_page_number else 2

            next_page_url = f"{response.request.url[:-1]}{next_page_number}"
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                meta={"current_page_number": next_page_number},
            )
