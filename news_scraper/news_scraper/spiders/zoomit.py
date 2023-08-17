from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from news_scraper.items import NewsItem
from scrapy.loader import ItemLoader
import scrapy

#scrapy spider that crawls main_url and extracts about 1000 recent news(last month news) articls url.
#after the news articles urls are extracted then crawls each url and extracts news data.
#then a NewsItem will be created by provided data and this item will be saved to database by piplines.
class QuotesSpider(scrapy.Spider):
    name = "zoomit"
    def __init__(self):
        self.main_url = 'https://www.zoomit.ir/archive'
        self.driver = webdriver.Firefox()
        self.more_button_press_count = 35
        self.parse_data = {
            #this dictionary contains selectors for news extraction in zoomit.ir and zoomg.ir.
            'zoomit' : {
                'title' : 'title::text',
                'text' : '.aMVhn::text , .hmanpw::text , .gOVZGU::text , .jktuKq::text',
                'tags' : '.eMeOeL::text',
                'video_tags' : '.jaRosJ::text'
            },
            'zoomg' : {
                'title' : 'title::text',
                'text' : '#bodyContainer li::text , strong::text , p::text',
                'tags' : '.GroupName::text',  
            },
        }
        self.more_button_css = '.eByvXQ .eEklvK'
        self.news_css_selector = '.iCQspp'
        self.video_element_xpath = '//*[@id="__next"]/div[2]/div[1]/main/article/div[4]/div/div/p[2]/a/strong'

    def start_requests(self):
        self.driver.get(self.main_url)
        count = 0
        for button_press in range(self.more_button_press_count):
            try:
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.more_button_css))).click()
            except:
                print('More news button not found!')
                raise 
        a_tag_elements = self.driver.find_elements(By.CSS_SELECTOR, self.news_css_selector)
        urls = [element.get_attribute('href') for element in a_tag_elements]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        domain = response.url[8:].split('/')[0].split('.')[1]
        loader = ItemLoader(item=NewsItem(), response=response)
        source = response.url
        if(domain == 'zoomit' or domain == 'zoomg'):
            parse_data = self.parse_data[domain]
            loader.add_css('title', parse_data['title'])
            loader.add_css('text', parse_data['text'])
            if(domain == 'zoomg'):
                loader.add_css('tags', parse_data['tags'])
            else:
                video_elements = response.xpath(self.video_element_xpath)
                if(len(video_elements) == 0):
                    loader.add_css('tags', parse_data['tags'])
                else:
                    loader.add_css('tags', parse_data['video_tags'])
        loader.add_value('source', response.url)
        yield loader.load_item()