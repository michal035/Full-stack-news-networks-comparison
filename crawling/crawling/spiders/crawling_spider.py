from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import requests
import random
import pandas as pd


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
    start_urls = ["http://ipinfo.io/ip"]
    

    rules = (
        Rule(LinkExtractor(allow="/", deny="category"), callback="parse_item"),
    )



    df = pd.read_csv('/home/michal/Documents/Python/scraping/test/crawling/proxy/working_proxies.csv', sep=" ") 

    l = len(df.index)
    random_proxy = df.iloc[random.randint(0, l-1)][0]

    CUSTOM_PROXY = f"http://{random_proxy}"


    def start_requests(self):
        for url in self.start_urls:
            re =  Request(url=url, callback=self.parse_item)
            re.meta["proxy"] = self.CUSTOM_PROXY

            yield re
                   
    
    def parse_item(self, response):
        yield {
            "IP" : response.body,
           
        }

        