# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.item import Item, Field


def format_price(price):
    return int(float(price.replace(",", "").replace("₹", "")))


class PartScraperItem(Item):
    
    # define the fields for your item here like:
    name = Field(output_processor=TakeFirst())
    price = Field(
        input_processor=MapCompose(format_price), output_processor=TakeFirst()
    )
    url = Field(output_processor=TakeFirst())
    store = Field(output_processor=TakeFirst())
    pass
