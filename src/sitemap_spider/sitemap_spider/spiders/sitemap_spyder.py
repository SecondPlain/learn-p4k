#
# sitemap_spider.py
#   Spider class for crawling Pitchfork's sitemap(using scrapy) 
#
#
import scrapy
import re
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector
from sitemap_spider.items import P4KSitemapItem
from scrapy.shell import inspect_response

class P4K_SitemapSpider(SitemapSpider):
    
    name = "sitemap"
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
        # objects. Elements of item_list are:
        #  0. review
        #  1. title
        #  2. artist
        #  3. score
        #  4. bnm_label
        #  5. author
        #  6. date
        #  7. label
        #  8. year
        item_list1 = []
        item_list1.append(response.selector.xpath('//div [@class="editorial"]').extract()[0])
        item_list1.append(divs.xpath('.//h2').extract()[0])
        item_list1.append(divs.xpath('.//h1').extract()[0])
        item_list1.append(divs.xpath('.//span').extract()[1])
        item_list1.append(divs.xpath('.//div [@class="bnm-label"]').extract()[0])
        item_list1 += divs.xpath('.//h4').extract()[0].split('; ')
        item_list1 += divs.xpath('.//h3').extract()[0].split('; ')
        
        # Remove tags, convert to unicode string, strip whitespace
        item_list = []
        for item in item_list1:
            item = item.encode('utf-8')
            item = re.sub('<[^>]*>', '', item)
            item = item.strip()
            item_list.append(item)

        # Load items
        item = P4KSitemapItem()
        item['review'] = item_list[0]
        item['title'] = item_list[1] 
        item['artist'] = item_list[2] 
        item['score'] = float(item_list[3])              # Convert score to float
        item['bnm_label'] = item_list[4] 
        item['author'] = item_list[5].replace('By ', '') # Only save author's name
        item['date'] = item_list[6] 
        item['label'] = item_list[7] 
        item['year'] = int(item_list[8])                 # Convert year to integer

        # For debug
#        inspect_response(response)

        yield item
        
        pass


