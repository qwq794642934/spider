# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider
from ..items import NovelItem
import re


class BiqukanSpider(RedisCrawlSpider):
    name = 'biqukan_redis'
    redis_key ='biqukan:start_urls'

    rules = (
        Rule(LinkExtractor(allow=(r'/\d+_\d+/'), deny=(r'/\d+\.html')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        items = NovelItem()
        items['book_id'] = response.url.split('/')[-2]
        items['book'] =  re.findall('<h2>(.*?)</h2>', response.text, re.S )[0]
        items['author'] = re.findall('<span>作者：(.*?)</span>',response.text, re.S )[0]
        items['category'] = re.findall('<span>分类：(.*?)</span>',response.text, re.S )[0]
        items['status'] = re.findall('<span>状态：(.*?)</span>',response.text, re.S )[0]
        items['count'] = re.findall('<span>字数：(.*?)</span>',response.text, re.S )[0]
        items['profile'] = re.findall('<span>简介：</span>(.*?)<br>',response.text, re.S )[0]
        chapter_list = response.xpath('//dd/a/@href').extract()[12:]
        for url in chapter_list:
            fullUrl = 'https://www.biqukan.com' + url
            yield scrapy.Request(url=fullUrl, callback=self.parse_chapter, meta={'items': items})


    def parse_chapter(self, response):
        items = response.meta.get('items')
        items['chapter_name'] = response.xpath('//h1/text()').extract_first()
        items['chapter_content'] = '\n'.join(response.xpath('//div[@id="content"]/text()').extract()[:-2]).replace('\u3000', '')
        yield items
        