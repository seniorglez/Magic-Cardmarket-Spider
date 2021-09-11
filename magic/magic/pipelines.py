# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from magic.shared.DBConnector import DBConnector
from magic.items import MagicCardMarketInformation, MagicCardMarketOffer


class MKMPipeline:

    def open_spider(self, spider):
        self.con = DBConnector('mkm')

    def process_item(self, item, spider):
        if isinstance(item, MagicCardMarketInformation):
            self.con.push(item, 'MKMInformation')
        elif isinstance(item, MagicCardMarketOffer):
            self.con.push(item, 'MKMOffer')
        else:
            logger.info("Unknow item instance")

        return item
