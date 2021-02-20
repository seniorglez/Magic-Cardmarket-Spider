from scrapy import Item, Field

class MagicItem(Item):
    url = Field(type=str)
    name = Field(type=str)
    number = Field(type=str)
    card_set = Field(type=str)

    #price
    minimun = Field(type=float)
    price_trend = Field(type=float)
    average_price_30_days = Field(type=float)
    average_price_7_days = Field(type=float)
    average_price_1_day = Field(type=float)