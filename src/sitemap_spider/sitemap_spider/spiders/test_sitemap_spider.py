#
# test_sitemap_spider.py
#   teset spider class for crawling Pitchfork's sitemap(using scrapy) and storing one album review in a file
#
#
import scrapy
from sitemap_spider.items import P4KSitemapItem
import re
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector


class P4K_SitemapSpider(SitemapSpider):
    name = "test_sitemap"
    sitemap_urls = ['http://www.pitchfork.com/sitemap-album-reviews.xml']

    #parse this particular album review and write the paragraph contents to a file
    #sitemap_rules = [('/19982-diarrhea-planet-aliens-in-the-outfield-ep/', 'parse_and_save')]
    sitemap_rules = [('/20021-andy-stott-faith-in-strangers/', 'parse_and_save')]

    def clean (self, string):
        
        #replace special characters with appropriate substitutions
        string = string.replace("u2014"," -- ")
        string = string.replace("u2013","-")
        string = string.replace("xa0", " ")
        string = string.replace("u2019", "'")
        string = string.replace("xe9", "e")
        string = string.replace("u2018", "'")
        
        #find tags and remove them
        string = re.sub('<[^>]*>', '', string)        
        
        #remove characters from the start and end of review
        string = string.replace("[u\' ", "")
        string = string.replace("\']", "")
        
        #remove all escape characters
        string = string.replace("\\", "")        
        
        return string
    
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
        review = (response.selector.xpath('//div [@class="editorial"]').extract().__str__());

        #clean the contents of the review
        review = self.clean(review)
        
        print review
        
        # Now we open a file with the new name and write the paragraph content 
        # to that file. Also converts the list object to a string
        with open(filename, 'wb') as f:
            f.write(review);

        ###########################

        #extract info inside <div class="info">
        divs = response.selector.xpath('//div [@class="info"]')

        ###########################
        
        #find the title
        #extract the first <h2> tags inside divs
        title =  ((divs.xpath('.//h2')).extract())[0]
        #remove tags from title
        #title = re.sub('<[^>]*>', '', title)
        title = title.__str__()
        title = self.clean(title)

        ###########################
        
        #find the artist
        artist =  ((divs.xpath('.//h1')).extract())[0]
        #artist = re.sub('<[^>]*>', '', artist)
        artist = artist.__str__()
        artist = self.clean(artist)

        ###########################

        #find the score
        score = ((divs.xpath('.//span')).extract())[1]
        #score = re.sub('<[^>]*>', '', score)
        score = score.__str__()
        score = self.clean(score)

        ###########################

        #find the review date
        date = ((divs.xpath('.//span')).extract())[0]
        date = re.sub('<[^>]*>', '', date)
        date = date.__str__()

        ###########################

        #find the bnm label
        bnm = ((divs.xpath('.//div [@class="bnm-label"]')).extract())[0]
        bnm = re.sub('<[^>]*>', '', bnm)
        if (bnm == " Best New Music "):
            is_bnm = True
            
        else:
            is_bnm = False

        ###########################

        #find the review author
        author = ((divs.xpath('.//h4')).extract())[0]
        author = re.sub('<[^>]*>', '', author)
        #remove the publication date after the semicolon
        author = re.sub(';.*', '', author)
        author = author.replace(" By ", "")
        author = author.__str__()

        ###########################

        #find the album year
        year = ((divs.xpath('.//h3')).extract())[0]
        year = re.sub('<[^>]*>', '', year)
        year = re.sub('.*; ', '', year)
        year = year.__str__()

        ###########################

        #find the record label
        label = ((divs.xpath('.//h3')).extract())[0]
        label = re.sub('<[^>]*>', '', label)
        label = re.sub(';.*', '', label)
        label = label.__str__()

        ###########################

        # The XML file we're working with has a nonstandard namespace -- you
        # can see it if you open up the file 'sitemap-album-reviews.xml' in 
        # directory src/crawl_p4k/ after running this spider. If we remove the
        # namespace, we can refer to the XML tags in the way you see in the
        # tutorial.
        response.selector.remove_namespaces()

        ###########################

        item = P4KSitemapItem()
        item['review'] = review.replace("\\","")
        item['title'] = title
        item['artist'] = artist
        item['score'] = score
        item['date'] = date
        item['is_bnm'] = is_bnm
        item['author'] = author
        item['year'] = year
        item['label'] = label
        yield item
        

        pass


