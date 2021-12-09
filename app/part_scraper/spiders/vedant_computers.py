import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem

CATEGORIES = [
    # "peripherals",
    # "networking",
    # "power-supply",
    # "fans-and-cooling",
    # "storage",
    # "monitor",
    "graphics-card",
    # "memory",
    # "processor",
    # "motherboard",
    # "cabinet",
]

PRODUCTS_LIMIT = 100


class VedantComputersSpider(scrapy.Spider):
    name = "vedant_computers"
    allowed_domains = ["vedantcomputers.com/pc-components/"]
    start_urls = [
        f"https://www.vedantcomputers.com/pc-components/{category}?limit={PRODUCTS_LIMIT}&page=1"
        for category in CATEGORIES
    ]

    def parse(self, response):

        # Check if the page has any results i.e. if the div with the "product-grid" class exists.
        items = response.css(".main-products.product-grid .caption")

        if items:

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

            # Scraping next pages
            # Check if the "page_no" variable exists.
            # If it doesn't exist, we are on the first page and we thus assign it the value 2.
            page_no = response.meta.get("page_no")
            page_no = int(page_no) + 1 if page_no else 2

            # Remove the part of the url that has the previous page number and append the new one.
            next_page_url = f"{response.request.url.rpartition('=')[0]}={page_no}"
            if next_page_url:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(
                    url=next_page_url, callback=self.parse, meta={"page_no": page_no}
                )
