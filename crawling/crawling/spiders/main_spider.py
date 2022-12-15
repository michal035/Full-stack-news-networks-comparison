from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import scrapy

import pandas as pd
import random

#In future it might be needed to outsource getting random proxy to separate file



base = "https://tvn24.pl/najnowsze/{}"
class CrawlingSpider(CrawlSpider):
    name = "stvn"
    allowed_domains = ["tvn24.pl"]
    start_urls = [base.format(i+1) for i in range(8) ]
    
    rules = (
        Rule(LinkExtractor(allow="najnowsze", deny="tvnwarszawa"), callback="parse_item"),
    )
    
    #I'm not sure why full path is needed - otherwise it won't work
    
    df = pd.read_csv('/home/michal/Documents/Python/scraping/test/crawling/proxy/working_proxies.csv', sep=" ") 

    l = len(df.index)
    random_proxy = df.iloc[random.randint(0, l-1)][0]
    CUSTOM_PROXY = f"http://{random_proxy}"
    #CUSTOM_PROXY = "https://195.154.255.194:8000"


    def start_requests(self):
        for url in self.start_urls:
            re =  Request(url=url, callback=self.parse_item)
            re.meta["proxy"] = self.CUSTOM_PROXY


            # Set the headers here. 
            headers =  {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.eventscribe.com',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpsRequest'
            }
            # Send the request
            scrapy.http.Request(url, method='GET' , headers = headers,  dont_filter=False)

            yield re


    def parse_item(self, response):
        yield {
            "HEADER" : response.css("h2::text").getall(),
            "HOUR": response.css(".label-date::text").getall()
           
        }


