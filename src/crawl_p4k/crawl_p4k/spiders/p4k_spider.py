#
# p4k_spider.py
#   Spider class for crawling Pitchfork's sitemap (using scrapy) 
#

import re
import scrapy
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector
from crawl_p4k.items import P4kSpiderItem

class P4kSpider(SitemapSpider):
    
    name = "p4k"
    sitemap_urls = ['http://www.pitchfork.com/sitemap-album-reviews.xml']
    #sitemap_urls = ['file:///home/jonathan/repo/learn-p4k/data/sitemap-test.xml']

    def parse(self,response):

        item = P4kSpiderItem()

        # Get review
        data = response.selector.xpath('//div [@id="main"]/div [@class="object-detail"]/div [@class="editorial"]')
        item['review'] = data.extract()

        # Get review meta-data
        meta = response.selector.xpath('//div [@id="main"]/ul [@class="review-meta"]')
        item['title'] = meta.xpath('.//div [@class="info"]/h2').extract()
        item['artist'] = meta.xpath('.//div [@class="info"]/h1').extract()
        item['score'] = meta.xpath('.//div [@class="info"]/span').extract()
        item['bnm_label'] = meta.xpath('.//div [@class="info"]/div [@class="bnm-label"]').extract()
        # Next part is tricky...
        authors_and_dates = meta.xpath('.//div [@class="info"]/h4').extract()
        item['author'] = []
        item['date'] = []
        for entry in authors_and_dates:
            author, date = entry.replace('&amp;', '&').split('; ')
            item['author'].append(author)
            item['date'].append(date)
        labels_and_years = meta.xpath('.//div [@class="info"]/h3').extract()
        item['label'] = []
        item['year'] = []
        for entry in labels_and_years:
            label, year = entry.replace('&amp;', '&').split('; ')
            item['label'].append(label)
            item['year'].append(year)
        
        # Remove tags, strip whitespace, fix ampersand characters
        for key in item.keys():
            for i in range(len(item[key])):
                item[key][i] = re.sub('<[^>]*>', '', item[key][i])
                item[key][i] = item[key][i].strip()
                item[key][i] = item[key][i].replace('&amp;', '&')

        # Only save author's name
        for i in range(len(item['author'])):
            item['author'][i] = item['author'][i].replace('By ', '')

#        # Debug
#        from scrapy.shell import inspect_response
#        inspect_response(response)

#        # Albums can have multiple artists, can be released by multiple labels,
#        # and can be (re)issued in multiple years. Pitchfork delimits metadata
#        # for multiple artists and labels with ' / ', but delimits multiple
#        # release years with just '/'.
#        keys = ('artist', 'label', 'year')
#        delims = (' / ', ' / ', '/')
#        for i in range(len(keys)):
#            expanded_list = []
#            for cur_item in item[keys[i]]:
#               expanded_list.append(cur_item.split(delims[i]))
#            item[keys[i]] = expanded_list
#
#        # Convert score and release year to numeric types
#        item['score'] = float(item['score'])
#        item['year'] = map(int, item['year'])

        yield item
        
        pass

