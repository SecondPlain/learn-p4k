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
        """ 
        The contents of this method tell the spider what to do with the data it
        encounters.
        """

        # A response is a scrapy object (class). One of its members is
        # the url of the webpage it found. Another is the content of the page.
        # The lines below get the url, split it at every '/' character, and 
        # writes the page content to a file.

        # This splits 'http://pitchfork.com/sitemap-album-reviews.xml' into
        # [http, , pitchfork.com, sitemap-album-reviews.xml],
        # then stores the last entry of the above list in the variable
        # called 'filename'.
        filename = response.url.split("/")[-1]
        
        # Now we open a file with the new name and write the page contents 
        # to that file.
        with open(filename, 'wb') as f:
            f.write(response.body)

        # The XML file we're working with has a nonstandard namespace -- you
        # can see it if you open up the file 'sitemap-album-reviews.xml' in 
        # directory src/crawl_p4k/ after running this spider. If we remove the
        # namespace, we can refer to the XML tags in the way you see in the
        # tutorial.
        response.selector.remove_namespaces()
