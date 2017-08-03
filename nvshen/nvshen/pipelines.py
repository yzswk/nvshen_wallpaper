# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from fake_useragent import UserAgent
ua = UserAgent()
headers = {"User-Agent": ua.chrome,
"Referer":"http://www.nvshens.com"}
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        filename = request.meta['name']
        # filespath = item['name'][0]
        # image_guid = request.url.split('/')[-1]
        # # return 'full/{}/{}' .format(filespath,image_guid)
        return filename

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,headers = headers,meta={'item': item, 'name': item['name'][0]})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
#
# from scrapy.pipelines.images import ImagesPipeline
#
# from scrapy.exceptions import DropItem
#
# from scrapy.http import Request
#
# headers = {
#
# "User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like
#
# "Referer":"http://xxxx.xxxx.com", #加入referer 为下载的域名网站
#
# }
#
# class MyImagesPipeline(ImagesPipeline):
#
# def get_media_requests(self, item, info):
#
# for image_url in item['image_urls']:
#
# yield Request(image_url,headers = headers)
#
# def item_completed(self, results, item, info):
#
# image_paths = [x['path'] for ok, x in results if ok]
#
# if not image_paths:
#
# raise DropItem("Item contains no images")
#
# item['image_paths'] = image_paths
#
# return item
