#
# p4k_spider.py
#   Spider class for crawling Pitchfork (using scrapy)
#
# Author
#   Jonathan D. Jones
#

import scrapy

class P4kSpider(scrapy.Spider):
    name = "p4k"
    allowed_domains = ["pitckfork.com"]
    start_urls = ["http://pitchfork.com/sitemap-album-reviews.xml"]

    def parse(self, response):
        filename = response.url.split("/")[0]
        with open(filename, 'wb') as f:
            f.write(response.body)
