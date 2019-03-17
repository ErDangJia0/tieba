# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import os


class TiebaPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_link = item['url']
        yield scrapy.Request(image_link)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results
                      if ok]
        newFolder = self.IMAGES_STORE + '/'+item['tName']

        if not os.path.exists(newFolder):
            os.mkdir(newFolder)
        os.rename(self.IMAGES_STORE + '/' + image_path[0], newFolder + '/' + image_path[0][5:])
        item['path'] = newFolder + '/' + image_path[0][5:]
        return item
