# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

#this pipeline saves provided news data to database.
#every time this pipline is used it creates a file named "items.json".
#then every NewsItem that is passed to process_item() function will be added to a list.
#then this list will be saved in "items.json" file.
class NewsPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')
        self.news_data = []

    def close_spider(self, spider):
        json.dump(self.news_data, self.file, ensure_ascii=False, indent=4)
        self.file.close()

    def process_item(self, item, spider):
        item.setdefault('title', None)
        item.setdefault('text', None)
        item.setdefault('tags', None)
        news_item = ItemAdapter(item).asdict()
        self.news_data.append(news_item)
        return item