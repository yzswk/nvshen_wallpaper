# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import NvshenItem
from scrapy import Request

page = 23506
class NvshenspiSpider(scrapy.Spider):
    name = 'nvshenspi'
    allowed_domains = ['www.nvshens.com']
    start_urls = ['https://www.nvshens.com/g/23506/']



    def parse(self, response):
        item = NvshenItem()
        name_list = response.xpath('//ul[@id="hgallery"]/img/@alt').extract()
        for name in name_list:
            item['name'] = [name]
            yield item
        img_list = response.xpath('//ul[@id="hgallery"]/img/@src').extract()
        for img in img_list:
            imgr = img.replace('/s/','/')
            item['image_urls'] = [imgr]
            yield item

        next_page = response.xpath('//div[@id="pages"]/a/@href').extract().pop()
        global page
        if next_page is not None and next_page != '/g/%d' % page:

            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse, dont_filter=True)
        else:
            page = page - 1
            next_page = '/g/%d' % page

            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse, dont_filter=True)
