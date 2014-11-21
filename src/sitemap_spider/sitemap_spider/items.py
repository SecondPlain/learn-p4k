# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class P4KSitemapItem(scrapy.Item):
    artist = scrapy.field()     # Album artist
    title = scrapy.field()      # Album title
    label = scrapy.field()      # Record label
    year = scrapy.field()       # Release year (or year of reissue)
    author = scrapy.field()     # Author of review
    score = scrapy.field()      # Score (0.0 - 10.0)
    is_bnm = scrapy.field()     # Best new music? (boolean)
    date = scrapy.field()       # Review date
    review = scrapy.field()     # Review content
    pass
