# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose
import scrapy

def format_price(price):
    return int(price.replace(",", "").replace("₹", ""))

class PartScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field(input_processor = MapCompose(format_price))
    url = scrapy.Field()
    pass
