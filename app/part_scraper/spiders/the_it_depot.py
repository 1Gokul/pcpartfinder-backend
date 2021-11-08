from time import sleep
import scrapy
from scrapy.loader import ItemLoader

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
    start_urls = [
        f"https://www.theitdepot.com/products-{category}.html"
        for category in CATEGORIES
    ]

    def parse(self, response):

        items = response.css(".product-item")

        for item in items:

            # Don't add the item to the database if it is listed as "Out of Stock"
            # The IT Depot website does not have an option to filter out out-of-stock items. :shrug:
            out_of_stock = item.css(
                "div.product-details span.text-danger::text"
            ).extract_first()

            if not out_of_stock:
                url = item.css("div.product_title a::attr(href)").extract_first()

                loader = ItemLoader(item=PartScraperItem(), selector=item)
                loader.add_css("name", "div.product_title a::text")
                loader.add_css(
                    "price",
                    "div.product-details > .card-text > strong::text",
                )
                loader.add_value("url", response.urljoin(url))
                loader.add_value("store", "IT_Depot")

                yield loader.load_item()

        """
        The ITDepot site does not make it easy to use pagination and crawl multiple pages of requests.
        Unlike other sites which use simple links to go to the next pages, the ITDepot site sends a request
        to the server and receives a HTML response, which it uses to refresh the search results section of the same page.
        So this spider sends requests to the same URL and scrapes the data from the returned HTML.
        """

        # Check if the response has any metadata passed in by previous requests. 
        page_no = response.meta.get("page_no") 
        next_page_url_prefix = response.meta.get("url_prefix")
        next_page_url_suffix = response.meta.get("url_suffix")

        # If it doesn't, it means the crawler has scraped the first page of the category. 
        # It will then have to create the metadata to pass to further requests.
        if not page_no:

            # Get the amount of pages in the search results
            last_page_no = response.css(
                ".pagination > li:nth-last-child(3) > a::text"
            ).extract_first()

            # Get the current category of the items.
            category = (
                response.request.url.replace("https://www.theitdepot.com/products-", "")
                .replace(".html", "")
                .split("_")
            )

            category[1] = category[1].replace("C", "")

            # The page number will start from 1
            page_no = 1

            # The part of the URL before the page number
            next_page_url_prefix = (
                f"https://www.theitdepot.com/category_filter.php?categoryname={category[0]}&filter-limit=16"
                f"&filter-orderby=price_asc&filter_listby=Grid&brand_id=&category={category[1]}&subcategory=&clearence=&free_shipping="
                "&ctotal=5&btotal=21&price_range=300%3B22135&feature_filter0=10&feature_filter1=10&feature_filter2=8"
                "&feature_filter3=11&feature_filter4=7&pageno="
            )
            # The part of the URL after the page number
            next_page_url_suffix = (
                f"&fftotal=5&total_pages={last_page_no}&PageScrollProcess=No&PageFinished=No&filter=true",
            )

        # Increment the current page number to go to the next page.
        page_no += 1
        
        sleep(5)

        yield scrapy.Request(
            url=f"{next_page_url_prefix}{page_no}{next_page_url_suffix}",
            callback=self.parse,
            meta={
                "url_prefix": next_page_url_prefix,
                "page_no": page_no,
                "url_suffix": next_page_url_suffix,
            },
        )