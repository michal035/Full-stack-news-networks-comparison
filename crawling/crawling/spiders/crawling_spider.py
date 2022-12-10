from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
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
    allowed_domains = ["httpbin.org"]
    start_urls = ["https://httpbin.org/ip"]
    

    rules = (
        Rule(LinkExtractor(allow="/", deny="category"), callback="parse_item"),
    )

    CUSTOM_PROXY = "http://31.186.239.245:8080"


    def start_requests(self):
        for url in self.start_urls:
            re =  Request(url=url, callback=self.parse)
            re.meta["proxy"] = self.CUSTOM_PROXY
            yield re
                   
    
    def parse_item(self, response):
        yield {
            "ip" : response.body,
           
        }

        