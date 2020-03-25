# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class NovelPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['novel']
        self.collection = self.db['book']

    def process_item(self, item, spider):
        book ={
            'book_id': item['book_id'],
            'book': item['book'],
            'author': item['author'],
            'category': item['category'],
            'status': item['status'],
            'count': item['count'],
            'profile': item['profile'],
            'chapter_name': item['chapter_name'],
            'chapter_content': item['chapter_content']
        }
        self.collection.save(book)
        return item
