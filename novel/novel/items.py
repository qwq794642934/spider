# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    book_id = scrapy.Field()
    book = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    count = scrapy.Field()
    profile = scrapy.Field()
    chapter_list = scrapy.Field()
    pass

class NovelContentItem(scrapy.Item):
    book_id = scrapy.Field()
    chapter_number = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()
    pass