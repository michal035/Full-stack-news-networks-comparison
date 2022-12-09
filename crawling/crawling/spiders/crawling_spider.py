from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import shutil
import requests


class CrawlingSpider(CrawlSpider):
    name = "spider1"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    
    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item")
    )


    def parse_item(self, response):
        yield {
            "title" : response.css(".product_main h1::text").get(),
            "price" : response.css(".price_color::text").get(),
            "availabity" : response.css(".availability::text")[1].get().replace("\n","").replace(" ","")


        }


            
        
class CrawlingSpider(CrawlSpider):
    name = "spider2"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/"]
    
    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue/a-light-in-the-attic_1000/", deny="category"), callback="parse_item")
    )


    def parse_item(self, response):
        yield {
            "title" : response.css("img").get(),
           


        }

        