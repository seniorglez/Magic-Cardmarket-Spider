import scrapy

from datetime import datetime
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError

from mkm.items import MagicItem

class MkmSpider(scrapy.Spider):
 
    name = 'mkm'
    
    home = 'https://www.cardmarket.com'
    url = 'https://www.cardmarket.com/en/Magic/Products/Singles?idExpansion=0&idRarity=0&sortBy=name_asc&perSite=30'
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'DOWNLOAD_DELAY': 1.5,  
        'COOKIES_ENABLED': False,
        'HTTPCACHE_ENABLED': False,
        'FEED_FORMAT': 'json',
    }


    def __init__(self, *args, **kwargs):
        super(MkmSpider, self).__init__(*args, **kwargs)
        
    # Request search main page
    def start_requests(self):
        ''' This method is called by Scrapy when the spider is opened.
        '''
        return Request(self.url,
                    callback=self.process_form_listing,
                    dont_filter=True)

    def process_form_listing(self, response):
        ''' This function creates request for all the listing of all the mtg expansions in order to parse every 'singles card' posible. 
        @url https://www.cardmarket.com/en/Magic/Products/Singles?idExpansion=0&idRarity=0&sortBy=name_asc&perSite=30
        @returns items 0
        @returns request 1
        '''

        expansion_ids = response.xpath("//select[@name='idExpansion']/option[@value!=0]/@value").getall()
        for i in expansion_ids:
            yield Request(f'https://www.cardmarket.com/es/Magic/Products/Singles?idExpansion={i}&idRarity=0&perSite=30',callback=self.search_request)

    def search_request(self,response):
        '''This function parses a card adverts SERP.

        @url https://www.cardmarket.com/en/Magic/Products/Search?idCategory=0&idExpansion=1&idRarity=0&perSite=30
        @returns items 0
        @returns requests 0 30
        '''
        urls = response.xpath("//div[@class='table-body']//div[@class='col-10 col-md-8 px-2 flex-column align-items-start justify-content-center']/a/@href").getall()
        for url in urls:
            yield Request(self.home+url,
                        callback=self.parse_item)
        next_url = response.xpath("//a[@data-direction='next']/@href").get()
        if next_url:
            yield Request(self.home+next_url,
                        callback=self.search_request)
        
    
    def parse_item(self,response):
        ''' This function parses a card advert.

        @url https://www.cardmarket.com/en/Magic/Products/Singles/Kaldheim/Woodland-Chasm
        @returns items 1
        @returns requests 0
        @scrapes url name number card_set minimun price_trend average_price_30_days average_price_7_days average_price_1_day
        '''
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

        return item

    #parsers

    def __parse_name(self,response):
        return response.xpath('//h1/text()').get()

    def __parse_number(self,response):
        response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[2]/text()').get()

    def __parse_card_set(self,response):
        return response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[3]/div/a[2]/text()').get()
    
    def __parse_available_items(self,response):
        return int(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[4]/text()').get())

    def __parse_minimum_price(self,response):
        return self.__parse_euro_to_float(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[5]/text()').get())
       
    def __parse_price_trend(self,response):
        return self.__parse_euro_to_float(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[6]/span/text()').get())
      
    def __parse_average_price_30_days(self,response):
        return self.__parse_euro_to_float(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[7]/span/text()').get())

    def __parse_average_price_7_days(self,response):
        return self.__parse_euro_to_float(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[8]/span/text()').get())
       
    def __parse_average_price_1_day(self,response):
        return self.__parse_euro_to_float(response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[9]/span/text()').get())

    #utils

    def __parse_euro_to_float(self,string):
        return float(string.replace('€','').replace(',','.').strip()) if string else None