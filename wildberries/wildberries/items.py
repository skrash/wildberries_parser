# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WildberriesItem_product(scrapy.Item):
    product_name = scrapy.Field()

class WildberriesItem_urls(scrapy.Item):
    visited_url = scrapy.Field()
