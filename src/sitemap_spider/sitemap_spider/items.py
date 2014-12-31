# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class P4KSitemapItem(scrapy.Item):
    artist = scrapy.Field()     # Album artist
    title = scrapy.Field()      # Album title
    label = scrapy.Field()      # Record label
    year = scrapy.Field()       # Release year (or year of reissue)
    author = scrapy.Field()     # Author of review
    score = scrapy.Field()      # Score (0.0 - 10.0)
    bnm_label = scrapy.Field()  # Best new music label
    date = scrapy.Field()       # Review date
    review = scrapy.Field()     # Review content
    pass
