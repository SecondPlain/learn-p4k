#
# p4k_spider.py
#   Spider class for crawling Pitchfork's sitemap(using scrapy) 
#

import re
import scrapy
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector
from crawl_p4k.items import P4kSpiderItem

class P4kSpider(SitemapSpider):
    
    name = "p4k"
    sitemap_urls = ['http://www.pitchfork.com/sitemap-album-reviews.xml']

    def parse(self,response):

        # The XML file we're working with has a nonstandard namespace -- you
        # can see it if you open up the file 'sitemap-album-reviews.xml' in 
        # directory src/crawl_p4k/ after running this spider. If we remove the
        # namespace, we can refer to the XML tags in the way you see in the
        # tutorial.
        response.selector.remove_namespaces()
        
        # <div class="info"> holds most of the review's meta-data
        divs = response.selector.xpath('//div [@class="info"]')

        # Grab review parameters that are of interest to us. These are unicode
        # objects. Elements of cur_items are:
        #   0. review
        #   1. title
        #   2. artist
        #   3. score
        #   4. bnm_label
        #   5. author
        #   6. date
        #   7. label
        #   8. year
        cur_items = []
        cur_items.append(response.selector.xpath('//div [@class="editorial"]').extract()[0])
        cur_items.append(divs.xpath('.//h2').extract()[0])
        cur_items.append(divs.xpath('.//h1').extract()[0])
        cur_items.append(divs.xpath('.//span').extract()[1])
        cur_items.append(divs.xpath('.//div [@class="bnm-label"]').extract()[0])
        cur_items += divs.xpath('.//h4').extract()[0].split('; ')
        cur_items += divs.xpath('.//h3').extract()[0].split('; ')
        
        # Remove tags, strip whitespace
        for i in range(len(cur_items)):
            cur_items[i] = re.sub('<[^>]*>', '', cur_items[i])
            cur_items[i] = cur_items[i].strip()

        # Load items
        item = P4kSpiderItem()
        item['review'] = cur_items[0]
        item['title'] = cur_items[1]
        item['artist'] = cur_items[2].split(' / ')      # An album can have multiple artists
        item['score'] = cur_items[3]
        item['bnm_label'] = cur_items[4] 
        item['author'] = cur_items[5].replace('By ', '') # Only save author's name
        item['date'] = cur_items[6]
        item['label'] = cur_items[7]
        item['year'] = cur_items[8].split('/')          # Album can be reissued

        yield item
        
        pass

