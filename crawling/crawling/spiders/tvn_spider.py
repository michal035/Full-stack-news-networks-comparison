from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, signals
import scrapy
from pydispatch import dispatcher
import re as a

import pandas as pd
import random




class CrawlingSpider(CrawlSpider):
    
    
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        

    def spider_closed(self, spider):
        df3 = df3.sort_values(by=['link'])
        df3.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines3.csv', index=None, sep=';', mode='w')
    
    
    name = "stvn"
    allowed_domains = ["tvn24.pl"]

    number_of_pages = 8
    start_urls = ["https://tvn24.pl/najnowsze/{}".format(i+1) for i in range(number_of_pages) ]
    
    rules = (
        Rule(LinkExtractor(allow="najnowsze", deny="tvnwarszawa"), callback="parse_item"),
    )

    #I'm not sure why full path is needed - otherwise it won't work
    
    df = pd.read_csv('/home/michal/Documents/Python/scraping/test/crawling/proxy/working_proxies.csv', sep=" ") 

    l = len(df.index)
    random_proxy = df.iloc[random.randint(0, l-1)][0]
    #CUSTOM_PROXY = f"http://{random_proxy}"
    CUSTOM_PROXY = "http://134.238.252.143:8080"

    print(f"THE IP IS {CUSTOM_PROXY}")

    
    def start_requests(self):
        global df3
        df3 = pd.DataFrame({ 
        'article-headline' : [],
        'hour/date' : [],
        'link': []


        })

        df3.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines3.csv', index=None, sep=';', mode='w')

        for url in self.start_urls:
            re =  Request(url=url, callback=self.parse_item)
            re.meta["proxy"] = self.CUSTOM_PROXY


            # Set the headers here. 
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
            # Send the request
            scrapy.http.Request(url, method='GET' , headers = headers,  dont_filter=False)   
            
            yield re
        
        


    def parse_item(self, response):
        global df3
        
        headnline = response.css("h2::text").getall()
        hour = response.css(".label-date::text").getall()
        


        for i in range(len(hour)):
            df2 = pd.DataFrame({ 
            'article-headline' : [headnline[i]],
            'hour/date' : [[hour[i]]],
            'link' : [int(response.request.url.split("/")[len(response.request.url.split("/"))-1])]
             })
            #df3 = pd.concat([df3,df2], ignore_index=True)
            df2.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines3.csv', index=None,header=None, sep=';', mode='a')
            


        yield {
            "HEADLINE" : headnline,
            "HOUR": hour
           
        }




#alternative news from the first site
class stvn_e(CrawlSpider):
      
    name = "stvn_e"
    allowed_domains = ["tvn24.pl"]
   
    df = pd.read_csv('/home/michal/Documents/Python/scraping/test/crawling/proxy/working_proxies.csv', sep=" ") 

    l = len(df.index)
    random_proxy = df.iloc[random.randint(0, l-1)][0]
    #CUSTOM_PROXY = f"http://{random_proxy}"
    CUSTOM_PROXY = "http://134.238.252.143:8080"

    print(f"THE IP IS {CUSTOM_PROXY}")



    def start_requests(self):
        
        
        global df3
        df3 = pd.DataFrame({ 
        'article-headline' : []

        })

        df3.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines2.csv', index=None, sep=';', mode='w')
        url = "https://tvn24.pl/"


        re =  Request(url=url, callback=self.parse_item)
        re.meta["proxy"] = self.CUSTOM_PROXY


        # Set the headers here. 
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
        # Send the request
        scrapy.http.Request(url, method='GET' , headers = headers,  dont_filter=False)   
        
        yield re
    
        

    def parse_item(self, response):
        
        headnlines = response.css("h2::text").getall()
        

        for i in range(len(headnlines)):
            df2 = pd.DataFrame({
                "headline" : [headnlines[i]]
            })
            df2.to_csv(r'/home/michal/Documents/Python/scraping/test/crawling/data/headlines2.csv', index=None,header=None, sep=';', mode='a')
            

        yield {
            "HEADLINE" : headnlines,      
        }


#Like this is useless - i mean the FEEDS thing, since i have my own custom 'save to csv' system 


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        "FEEDS": {
            "crawling/other/items3.json": {"format": "json"},
        },
    })


    process.crawl(stvn_e)
    process.start() 
