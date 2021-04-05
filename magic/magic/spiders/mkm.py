import scrapy

from datetime import datetime
from scrapy import Request
from scrapy.selector import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from magic.items import MagicCardMarketInformation, MagicCardMarketOffer

class MkmSpider(scrapy.Spider):
 
    name = 'mkm'
    home = 'https://www.cardmarket.com'
    url = 'https://www.cardmarket.com/en/Magic/Products/Singles?idExpansion=0&idRarity=0&sortBy=name_asc&perSite=30'
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 5,
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
        yield Request(self.url,
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
            yield Request(f'https://www.cardmarket.com/en/Magic/Products/Singles?idExpansion={i}&idRarity=0&perSite=30',callback=self.search_request)

    def search_request(self,response):
        '''This function parses a card adverts SERP.

        @url https://www.cardmarket.com/en/Magic/Products/Search?idCategory=0&idExpansion=1&idRarity=0&perSite=30
        @returns items 0
        @returns requests 0 30
        '''
        urls = response.xpath("//div[@class='table-body']//div[@class='col-10 col-md-8 px-2 flex-column align-items-start justify-content-center']/a/@href").getall()
        for url in urls:
            yield Request(self.home+url,
                        callback=self.parse_items)
        next_url = response.xpath("//a[@data-direction='next']/@href").get()
        if next_url:
            yield Request(self.home+next_url,
                        callback=self.search_request)
            
    def parse_items(self,response):
        ''' This function parses a card advert.

        @url https://www.cardmarket.com/en/Magic/Products/Singles/Kaldheim/Woodland-Chasm
        @returns requests 0
        @scrapes url name set_number card_set minimun price_trend average_price_30_days average_price_7_days average_price_1_day
        '''
        info = MagicCardMarketInformation()
        
        info['url'] = response.url
        info['name'] = self.__parse_name(response)
        info['set_number'] = self.__parse_number(response)
        info['card_set'] = self.__parse_card_set(response)
       
        info['minimun'] = self.__parse_minimum_price(response)
        info['price_trend'] = self.__parse_price_trend(response)
        info['average_price_30_days'] = self.__parse_average_price_30_days(response)
        info['average_price_7_days'] = self.__parse_average_price_7_days(response)
        info['average_price_1_day'] = self.__parse_average_price_1_day(response)

        yield info

        for offer in self.__get_offers(response):
            yield self.__parse_offer(Selector(text=offer))
    
    def __get_offers(self,response):#this only will get the 25 first results, I will need to use JS to show all the results.
        ''' This function returns a list with all the offer html
        @url https://www.cardmarket.com/en/Magic/Products/Singles/Kaldheim/Woodland-Chasm
        @returns requests 0
        '''
        return response.xpath("//div[@class='table article-table table-striped']/div[@class='table-body']/div[@class='row no-gutters article-row']").getall()
    
    def __parse_offer(self,selector):
        item = MagicCardMarketOffer()
        item['country'] = self.__parse_country(selector)
        item['seller'] = self.__parse_seller(selector)
        item['card_condition'] = self.__parse_card_condition(selector)
        item['card_language'] = self.__parse_card_language(selector)
       #item['is_professional'] = self.
       #item['is_foil'] = self.
       #item['is_signed'] = self.
        item['is_playset'] = self.__parse_is_playset(selector)
       #item['product_comments'] = self.
       #item['price'] = self.
       #item['item_count'] = self.
        return item

    #parsers info

    def __parse_name(self,response):
        return response.xpath('//h1/text()').get()

    def __parse_number(self,response):
        return response.xpath('//dl[@class="labeled row no-gutters mx-auto"]//dd[2]/text()').get()

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

    #parsers offer

    def __parse_country(self,selector):
        return self.__parse_title_to_country(selector.xpath('//span[@class="seller-name d-flex"]/span[@class="icon d-flex has-content-centered mr-1"]/@title').get())

    def __parse_seller(self,selector):
        return selector.xpath('//span[@class="seller-name d-flex"]/span[@class="d-flex has-content-centered mr-1"]/a/text()').get()

    def __parse_card_condition(self,selector):
        return selector.xpath('//div[@class="col-sellerProductInfo col"]/div[@class="row no-gutters"]/div[2]//span[@class="icon"]/@data-original-title').get()

    def __parse_card_language(self,selector):
        return selector.xpath('//div[@class="col-sellerProductInfo col"]/div[@class="row no-gutters"]/div[2]//span[@class="icon mr-2"]/@data-original-title').get()

    def __parse_is_professional(self,selector):
        response=selector.xpath('//div[@class="col-sellerProductInfo col"]/div[@class="row no-gutters"]/div[2]//span[@class="icon st_SpecialIcon mr-1"]/@data-original-title').get()
        if response:
            return True
        return False

    def __parse_is_foil(self,selector):
        pass

    def __parse_is_signed(self,selector):
        pass

    def __parse_is_playset(self,selector):
        pass

    def __parse_price(self,selector):
        pass

    def __parse_item_count(self,selector):
        pass

    #utils

    def __parse_euro_to_float(self,string):
        return float(string.replace('€','').replace(',','.').strip()) if string else None
    
    def __parse_title_to_country(self,string):
        return string.replace('Item location:','').strip()