# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class M4JamItem(scrapy.Item):
    payload_id = scrapy.Field()
    entrance_picture = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    job_name = scrapy.Field()
