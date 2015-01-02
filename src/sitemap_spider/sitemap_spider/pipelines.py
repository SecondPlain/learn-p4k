# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# This pipeline writes the spider's output to a unicode-formatted json file.
# Right now the output file name is hardcoded in the __init__ method, but it
# should be changed to read from a configuration file. Most of this code was
# taken from this StackExchange post:
#
#     http://stackoverflow.com/questions/9181214/scrapy-text-encoding
#

import json
import codecs

class JsonUnicode(object):

    def __init__(self):
        self.file = codecs.open('p4k-all.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
