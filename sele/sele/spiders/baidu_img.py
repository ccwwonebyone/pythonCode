# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from sele.items import SeleItem


class BaiduImgSpider(scrapy.Spider):
    name = 'baidu_img'
    allowed_domains = ['']
    base_url = ''

    def start_requests(self):
        for page in range(1, 5):
            url = self.base_url + '?page=' + str(page)
            yield scrapy.Request(url = url, callback=self.parse,dont_filter=True )

    def parse(self, response):
        html = BeautifulSoup(response.text, 'html.parser')
        results = html.select('.card')
        for info in results:
            card_body = info.select('.card-body')
            item = SeleItem()
            if len(card_body) < 1:
                break
            item['title'] = card_body[0].select('.card-title')[0].find_all(text=True)[0]
            author_created_time = card_body[0].select('div')[-1].find_all(text=True)[1]
            author_created_time = author_created_time.strip().split(' ')
            item['author'] = author_created_time[0]
            item['created_time'] = author_created_time[1] + ' ' + author_created_time[2]
            yield item