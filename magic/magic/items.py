# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MagicCardMarketInformation(Item):
    url = Field(type=str)
    name = Field(type=str)
    set_number = Field(type=str)
    card_set = Field(type=str)

    #price
    minimun = Field(type=float)
    price_trend = Field(type=float)
    average_price_30_days = Field(type=float)
    average_price_7_days = Field(type=float)
    average_price_1_day = Field(type=float)

class MagicCardMarketOffer(Item):
    country = Field(type=str)
    seller = Field(type=str)
    card_condition = Field(type=str)
    card_language = Field(type=str)
    is_professional = Field(type=str)
    is_foil = Field(type=bool)
    is_signed = Field(type=bool)
    is_playset = Field(type=bool)
    product_comments = Field(type=str)
    price = Field(type=float)
    item_count = Field(type=int)