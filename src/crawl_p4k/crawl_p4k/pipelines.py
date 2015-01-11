# -*- coding: utf-8 -*-
#
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
# This pipeline writes the spider's output to a unicode-formatted json file.
# Right now the output file name is hardcoded, but it should be changed to read
# from a configuration file. This code was written with reference to the
# following StackExchange post (Warning, the spider_closed() method used in
# the link is deprecated):
#
#     http://stackoverflow.com/questions/9181214/scrapy-text-encoding
#

import json
import codecs
import os

class JsonUnicode(object):

    def __init__(self):
        # Open the file and write a [
        corpus_dir = '/home/jonathan/repo/learn-p4k/data/p4k/'
        self.filehandle = codecs.open(corpus_dir + 'p4k-all.json', 'w', encoding='utf-8')
        self.filehandle.write('[')
        self.is_first_item = True

    def process_item(self, item, spider):
        # Append dictionary representing current review
        line = json.dumps(dict(item), ensure_ascii=False)
        if not self.is_first_item:
            line = ",\n" + line
        self.filehandle.write(line)
        self.is_first_item = False
        return item

    def close_spider(self, spider):
        # Write a ] and close the file
        self.filehandle.write(']')
        self.filehandle.close()
        
