import scrapy

from datetime import datetime
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError

from mkm.items import MagicItem

class MkmSpider(scrapy.Spider):
 
    name = 'mkm'

    home='https://www.cardmarket.com'
    url = 'https://www.cardmarket.com/en/Magic/Products/Singles?idExpansion=0&idRarity=0&sortBy=name_asc&perSite=30'
    
    
    def __init__(self, *args, **kwargs):
        super(MkmSpider, self).__init__(*args, **kwargs)
        
    # Request search main page
    def start_requests(self):
        yield Request(self.url,
                    callback=self.search_request,
                    dont_filter=True)


    def search_request(self,response):
        urls = response.xpath("//div[@class='table-body']//div[@class='col-10 col-md-8 px-2 flex-column align-items-start justify-content-center']/a/@href").getall()
        for url in urls:
            yield Request(self.home+url,
                        callback=self.parse_item)
        next_url = response.xpath("//a[@data-direction='next']/@href").get()
        if next_url:
            yield Request(self.home+next_url,
                        callback=self.search_request)
        
    
    def parse_item(self,response):
        item = MagicItem()
        
        item['url'] = response.url
        item['name'] = self.__parse_name(response)
        item['number'] = self.__parse_number(response)
        item['card_set'] = self.__parse_card_set(response)
       
        item['minimun'] = self.__parse_minimum_price(response)
        item['price_trend'] = self.__parse_price_trend(response)
        item['average_price_30_days'] = self.__parse_average_price_30_days(response)
        item['average_price_7_days'] = self.__parse_average_price_7_days(response)
        item['average_price_1_day'] = self.__parse_average_price_1_day(response)

        yield item

    def __parse_name(self,response):
        return response.xpath('//h1/text()').get()

    def __parse_number(self,response):
        response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[2]/text()').get()

    def __parse_card_set(self,response):
        return response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[3]/div/a[2]/text()').get()
    
    def __parse_available_items(self,response):
        return int(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[4]/text()').get())

    def __parse_minimum_price(self,response):
        raw = response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[5]/text()').get()
        if raw:
            raw.replace(' €','')
            return float(raw)
        else: 
            return None


    def __parse_price_trend(self,response):
        raw = response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[6]/span/text()').get()
        if raw:
            raw.replace(' €','')
            return float(raw)
        else: 
            return None

    def __parse_average_price_30_days(self,response):
        raw = response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[7]/span/text()').get()
        if raw:
            raw.replace(' €','')
            return float(raw)
        else: 
            return None

    def __parse_average_price_7_days(self,response):
        raw = response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[8]/span/text()').get()
        if raw:
            raw.replace(' €','')
            return float(raw)
        else: 
            return None

    def __parse_average_price_1_day(self,response):
        raw = response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[9]/span/text()').get()
        if raw:
            raw.replace(' €','')
            return float(raw)
        else:
            return None


