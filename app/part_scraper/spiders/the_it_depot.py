from time import sleep
import scrapy
from scrapy.loader import ItemLoader

from part_scraper.items import PartScraperItem
from config import DB_CATEGORIES

SITE_CATEGORIES = [
    # "Computer+Cabinets_C5",
    # "Cooling+Devices_C10",
    "Graphic+Cards_C45",
    # "Hard+Drives+HDD_C12",
    # "Keyboards_C3",
    # "RAM+(Memory)_C6",
    # "Monitor_C7",
    # "Mouse+(Mice)_C1",
    # "PSU+(+Power+Supply+Units)_C14",
    # "Processors_C30",
    # "Solid+State+Drive+(SSD)_C93",
    # "Headphones_C19",
    # "Gaming+Headphones_C9SU16",
]


class ITDepotSpider(scrapy.Spider):
    name = "it_depot"
    allowed_domains = ["theitdepot.com"]
    start_urls = [
        f"https://www.theitdepot.com/products-{category}.html"
        for category in SITE_CATEGORIES
    ]

    def parse(self, response):

        # Get the current category of the items. It will be needed for the "category"
        # column in the database.
        # Check if it exists in the response meta, else extract it from the URL.
        category = response.meta.get("category")
        if not category:
            category = (
                response.request.url.replace("https://www.theitdepot.com/products-", "")
                .replace(".html", "")
                .split("_")
            )

            category[1] = category[1].replace("C", "")

        items = response.css(".product-item")

        for item in items:

            # Don't add the item to the database if it is listed as "Out of Stock"
            # The IT Depot website does not have an option to filter out out-of-stock items. :shrug:
            out_of_stock = item.css("div.product-details span.text-danger::text").get()

            if not out_of_stock:
                url = item.css("div.product_title a::attr(href)").get()

                loader = ItemLoader(item=PartScraperItem(), selector=item)
                loader.add_css("name", "div.product_title a::text")
                loader.add_css(
                    "price",
                    "div.product-details > .card-text > strong::text",
                )
                loader.add_value("url", response.urljoin(url))
                loader.add_value("category", DB_CATEGORIES[category[0]])
                loader.add_value("store", "IT_Depot")

                yield loader.load_item()

        """
        Unlike other sites which use simple links to go to the next pages, the ITDepot site sends a request
        to the server and receives a HTML response, which it uses to refresh the search results section of the same page.
        So this spider sends requests to the same URL and scrapes the data from the returned HTML.
        """

        # Check if the response has any metadata passed in by previous requests.
        page_no = response.meta.get("page_no")
        total_pages = response.meta.get("total_pages")
        next_page_url_prefix = response.meta.get("url_prefix")

        # If it doesn't, it means the crawler has scraped the first page of the category.
        # It will then have to create the metadata to pass to further requests.
        if not page_no:

            # Get the amount of pages in the search results
            total_pages = int(
                response.css(".pagination > li:nth-last-child(3) > a::text").get()
            )
            total_pages = int(total_pages) if total_pages else 0

            # The page number will start from 1
            page_no = 1

            # The part of the URL before the page number
            next_page_url_prefix = (
                f"https://www.theitdepot.com/category_filter.php?categoryname={category[0]}&filter-limit=16"
                f"&category={category[1]}&pageno="
            )

        # Increment the current page number to go to the next page.
        page_no += 1

        if page_no <= total_pages:

            yield scrapy.Request(
                url=f"{next_page_url_prefix}{page_no}&total_pages={total_pages}&filter=true",
                callback=self.parse,
                meta={
                    "url_prefix": next_page_url_prefix,
                    "page_no": page_no,
                    "total_pages": total_pages,
                    "category": category,
                },
            )
