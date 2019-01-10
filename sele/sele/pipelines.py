from pymongo import MongoClient
import json
import scrapy
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SelePipeline(object):
    
    def open_spider(self, spider):
        self.client = MongoClient('localhost')
        self.blog   = self.client.blog
        self.article = self.blog.article

    def process_item(self, item, spider):
        self.article.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
