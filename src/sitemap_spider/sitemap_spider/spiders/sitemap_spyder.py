#
# sitemap_spider.py
#   Spider class for crawling Pitchfork's sitemap(using scrapy) 
#
#
import scrapy
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector

class P4K_SitemapSpider(SitemapSpider):
    name = "sitemap"
    sitemap_urls = ['http://www.pitchfork.com/sitemap-album-reviews.xml']

    def parse(self,response):
        
        pass
    
"""
    def parse_and_save(self, response):
        
        
        # A response is a scrapy object (class). One of its members is
        # the url of the webpage it found. Another is the content of the page.
        # The lines below get the url, split it at every '/' character, and 
        # writes the page content to a file.

        # This splits 'http://pitchfork.com/sitemap-album-reviews.xml' into
        # [http, , pitchfork.com, sitemap-album-reviews.xml],
        # then stores the second last entry of the above list in the variable
        # called 'filename', and added the format .txt to it
        filename = response.url.split("/")[-2] + ".txt"
        
        # Now we open a file with the new name and write the page contents 
        # to that file. Also converts the list object to a string
        with open(filename, 'wb') as f:
            f.write((response.selector.xpath('//p/text()').extract()).__str__())

        # The XML file we're working with has a nonstandard namespace -- you
        # can see it if you open up the file 'sitemap-album-reviews.xml' in 
        # directory src/crawl_p4k/ after running this spider. If we remove the
        # namespace, we can refer to the XML tags in the way you see in the
        # tutorial.
        response.selector.remove_namespaces()

        pass
"""

