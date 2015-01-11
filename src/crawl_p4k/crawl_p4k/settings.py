# -*- coding: utf-8 -*-

# Scrapy settings for sitemap_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawl_p4k'

SPIDER_MODULES = ['crawl_p4k.spiders']
NEWSPIDER_MODULE = 'crawl_p4k.spiders'
ITEM_PIPELINES = ['crawl_p4k.pipelines.JsonUnicode']
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_p4k (+http://www.yourdomain.com)'
