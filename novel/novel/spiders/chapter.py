# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider
from ..items import NovelContentItem

class ChapterSpider(RedisSpider):
    name = 'chapter'
    redis_key= 'chapter:start_urls'

    def parse(self, response):
        items = NovelContentItem()
        items['book_id']  = response.url.split('/')[-2]
        items['chapter_number']  = response.url.split('/')[-1].split('.')[0]
        items['chapter_name'] = response.xpath('//h1/text()').extract_first()
        items['chapter_content'] = '\n'.join(response.xpath('//div[@id="content"]/text()').extract()[:-2]).replace('\u3000', '')
        yield items