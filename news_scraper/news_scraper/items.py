# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


class NewsItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst())
    
    text = scrapy.Field(
        output_processor=Join())
    
    tags = scrapy.Field()

    source = scrapy.Field(
        output_processor=TakeFirst())