#
# sitemap_spider.py
#   teset spider class for crawling Pitchfork's sitemap(using scrapy) and storing one album review in a file
#
#
import scrapy
import re
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector

class P4K_SitemapSpider(SitemapSpider):
    name = "test_sitemap"
    sitemap_urls = ['http://www.pitchfork.com/sitemap-album-reviews.xml']

    #parse this particular album review and write the paragraph contents to a file
    sitemap_rules = [('/19982-diarrhea-planet-aliens-in-the-outfield-ep/', 'parse_and_save')]



    def parse_and_save(self, response):
        """ 
        The contents of this method tell the spider what to do with the data it
        encounters.
        """
        
        # A response is a scrapy object (class). One of its members is
        # the url of the webpage it found. Another is the content of the page.
        # The lines below get the url, split it at every '/' character, and 
        # writes the page content to a file.

        # This splits the response
        # then stores the second last entry of the above list in the variable
        # called 'filename', and added the format .txt to it
        filename = response.url.split("/")[-2] + ".txt"
        text = (response.selector.xpath('//div [@class="editorial"]').extract().__str__());

        #replace u2014 with --
        text = text.replace("u2014","--");

        #remove characters from the start and end of text
        text = text.replace("[u\'", "")
        text = text.replace("\']", "")

        #find tags and remove them
        text = re.sub('<[^>]*>', '', text)
        
        #remove all escape characters
        text = text.replace("\\", "");
        
        # Now we open a file with the new name and write the paragraph content 
        # to that file. Also converts the list object to a string
        with open(filename, 'wb') as f:
            f.write(text);

        # The XML file we're working with has a nonstandard namespace -- you
        # can see it if you open up the file 'sitemap-album-reviews.xml' in 
        # directory src/crawl_p4k/ after running this spider. If we remove the
        # namespace, we can refer to the XML tags in the way you see in the
        # tutorial.
        response.selector.remove_namespaces()

        pass


