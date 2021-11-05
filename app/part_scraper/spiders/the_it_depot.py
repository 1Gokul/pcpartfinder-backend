import scrapy
from scrapy.loader import ItemLoader
from scrapy.shell import inspect_response

from part_scraper.items import PartScraperItem

CATEGORIES = [
    "Computer+Cabinets_C5",
    "Cooling+Devices_C10",
    "Graphic+Cards_C45",
    "Hard+Drives+HDD_C12",
    "Keyboards_C3",
    "RAM+(Memory)_C6",
    "Monitor_C7",
    "Mouse+(Mice)_C1",
    "PSU+(+Power+Supply+Units)_C14",
    "Processors_C30",
    "Solid+State+Drive+(SSD)_C93",
    "Headphones_C19",
    "Gaming+Headphones_C9SU16",
]


class ITDepotSpider(scrapy.Spider):
    name = "it_depot"
    allowed_domains = ["theitdepot.com"]
    start_urls = [f"https://www.theitdepot.com/products-{category}.html" for category in CATEGORIES]

    def parse(self, response):
        
        # inspect_response(response, self)
        items = response.css(".product-item")
        
        for item in items:

            # Don't add the item to the database if it is listed as "Out of Stock"
            # The IT Depot website does not have an option to filter out out-of-stock items. :shrug:
            out_of_stock = item.css("div.product-details span.text-danger::text").extract_first()

            if not out_of_stock:
                url = item.css("div.product_title a::attr(href)").extract_first()

                loader = ItemLoader(item=PartScraperItem(), selector=item)
                loader.add_css(
                    "name", "div.product_title a::text"
                )
                loader.add_css(
                    "price",
                    "div.product-details > .card-text > strong::text",
                )
                loader.add_value(
                    "url", response.urljoin(url)
                )
                loader.add_value("store", "IT_Depot")

                yield loader.load_item()


