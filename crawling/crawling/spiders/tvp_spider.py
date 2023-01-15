from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, signals
import scrapy
from pydispatch import dispatcher
import re as a

import pandas as pd
import random

#In future it might be needed to outsource getting random proxy to separate file ^

# maybe link for the article should be extracted as well



class stvp(CrawlSpider):
    
    
    name = "stvp"
    allowed_domains = "tvp.info"


    df = pd.read_csv('/home/michal/Documents/Python/scraping/test/crawling/proxy/working_proxies.csv', sep=" ") 

    l = len(df.index)
    random_proxy = df.iloc[random.randint(0, l-1)][0]
    #CUSTOM_PROXY = f"http://{random_proxy}"
    CUSTOM_PROXY = "http://134.238.252.143:8080"


    def start_requests(self):
        url="https://www.tvp.info/"
        re =  Request(url, callback=self.parse_item)
        re.meta["proxy"] = self.CUSTOM_PROXY



        df5 = pd.DataFrame({ 
        'article-headline' : [],
        'hour/date' : []
        })

        df5.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines5.csv', index=None, sep=';', mode='w')


        headers =  {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.eventscribe.com', #need to test if removing this would do anything
        'Referer': url, 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'X-Requested-With': 'XMLHttpsRequest'
        }

        scrapy.http.Request(url, method='GET' , headers = headers,  dont_filter=False)   
        
        yield re


    def parse_item(self, response):
        
        
        headlines = response.css(".news__title::text").getall()
        hours = response.css(".news__time::text").getall()


        for i in range(len(headlines)):
            headlines[i] = headlines[i].replace("\n","")
            headlines[i] = " ".join(headlines[i].split())

            hours[i] = " ".join(hours[i].split())
            hours[i] = hours[i].replace("\t","")


            df5 = pd.DataFrame({
            'article-headline' : [headlines[i]],
            'hour/date' : [hours[i]]
                
            })


            df5.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines5.csv', index=None,header=None, sep=';', mode='a')

        yield{

            "HEADLINES" : headlines,
            "TIME" : hours
        }

#Like this is useless - i mean the FEEDS thing, since i have my own custom 'save to csv' system 


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        "FEEDS": {
            "crawling/other/items.json": {"format": "json"},
        },
    })


    process.crawl(stvp)
    process.start() 
