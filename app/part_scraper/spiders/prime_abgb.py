import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
    "cpu-processor",
    "motherboards",
    "ram-memory",
    "cpu-cooler",
    "internal-hard-drive",
    "graphic-card-gpu",
    "pc-cases-cabinet",
    "led-monitors",
    "power-supplies-smps",
    "keyboard",
    "mouse-mice",
    "mouse-pad",
    "gaming-headset",
    "gaming-chair",
    "gaming-wireless-routers",
    "mic",
    "server-processor",
    "server-motherboard",
    "super-server",
    "server-chassis",
    "server-graphic-card",
    "server-memory",
    "enterprise-server-hard-drive",
    "enterprise-ssd",
    "network-attached-storage-nas",
]


class PrimeABGBSpider(scrapy.Spider):
    name = "prime_abgb"
    allowed_domains = ["primeabgb.com"]
    start_urls = [
        f"https://www.primeabgb.com/buy-online-price-india/{category}/?filters=_stock_status[instock]" for category in CATEGORIES
    ]

    def parse(self, response):

        items = response.css(".products .product-innfo")

        for item in items:
            loader = ItemLoader(item=PartScraperItem(), selector=item)
            loader.add_css("name", "h3.product-name a::text")
            loader.add_css("price", "div.product-innfo > span > ins > span > bdi::text")
            loader.add_css("url", "h3.product-name a::attr(href)")
            loader.add_value("store", "Prime_ABGB")

            yield loader.load_item()


        # Goes to the next page using the pagination links at the bottom
        next_page_url = response.css(".page-numbers > li:nth-last-child(1) > a::attr(href)").extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
