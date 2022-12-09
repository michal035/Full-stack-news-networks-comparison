from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



base = "https://tvn24.pl/najnowsze/{}"
class CrawlingSpider(CrawlSpider):
    name = "stvn"
    allowed_domains = ["tvn24.pl"]
    start_urls = [base.format(1)]
    
    rules = (
        Rule(LinkExtractor(allow="najnowsze", deny="tvnwarszawa"), callback="parse_item"),
    )


    def parse_item(self, response):
        yield {
            "HEADER" : response.css("h2::text").getall(),
            "HOUR": response.css(".label-date::text").getall()
           
        }


