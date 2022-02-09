from scrapy import Spider, Request
from bs4 import BeautifulSoup
from wildberries.items import WildberriesItem_product, WildberriesItem_urls
import hashlib
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
import sqlite3 as sql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WbSpider(Spider):
    name = 'wb'
    allowed_domains = ['wildberries.ru']
    start_urls = ['https://www.wildberries.ru']
    visited = []
    products = dict()
    urls = dict()

    def check_detected_scraping(self, soup):
        pass
        # if soup.find('div', {'class': 'error500'}) is not None:
        #     self.log('------------------------------------------------------------------------------------------------')
        #     self.log('SCRAPPER DETECTED ! OMG O_O')
        #     self.log('------------------------------------------------------------------------------------------------')
        #     self.reopen_browser()

    def check_condition_cards(self, soup):
        self.log('------------------------------------------------------------------------------------------------')
        self.log('CHECK CONDITION CARDS')
        self.log('------------------------------------------------------------------------------------------------')
        # cards = soup.findAll('div', {'class':'product-card'})
        cards = soup.findAll('a', {'class': 'product-card__main j-card-link'})
        if cards is None or len(cards) < 1:
            cards = soup.findAll('a', {'class': 'product-card__main j-card-link'})
        if cards is None or len(cards) < 1:
            cards = soup.findAll('li', {'class': 'goods-card'})
        return cards

    def check_condition_products(self, soup, card):
        self.log('<------------------------------------------------------------------------------------------------')
        product_name = card.find('p', {'class': 'goods-card__description'})
        product_price = card.find('span', {'class': 'goods-card__price-now'})
        if product_name is None or product_name is None:
            card_desc = card.find('div', {'class': 'product-card__brand'})
            self.log('CARD DESK IS ' + str(card_desc))
            if product_name is None:
                product_name = card_desc.find('div', {'class': 'product-card__brand-name'}).text
            if product_price is None:
                product_price = card_desc.find('ins', {'class': 'lower-price'}).text
            if product_name is None:
                product_name = card_desc.find('span', {'class': 'goods-name'}).text
            if product_price is None:
                product_price = card_desc.find('span', {'class': 'price'}).text

        self.log('------------------------------------------------------------------------------------------------')
        self.log('INNER CONDITION: ' + str(product_name) + ' ' + str(product_price))
        self.log('------------------------------------------------------------------------------------------------')
        # if isinstance(type(product_name), type(None))  or len(product_name) < 1:
        #     product_name = card.find('div', {'class': 'product-card__brand'}).find('div', {'class': 'product-card__brand-name'}).text
        # product_price = card.find('ins', {'class': 'lower-price'}).text
        # if isinstance(isinstance(type(product_price), type(None)) or len(product_price) < 1):
        #     product_price = card.find('div', {'class': 'product-card__price'}).text
        # if isinstance(isinstance(type(product_price), type(None)) or len(product_price) < 1):
        #     product_price = card.find('div', {'class': 'product-card__price'}).find
        return [product_name, product_price]

    def write_db(self):
        for product in self.products.items():
            print('PRODUCTS: ', product)
            try:
                connection = sql.connect('wildberries.db')
                with connection:
                    cursor = connection.cursor()
                    cursor.execute('INSERT INTO products values (?,?)', tuple(product))
                    connection.commit()
            except Exception as e:
                self.log('НЕ УДАЛОСЬ ЗАПИСАТЬ В БАЗУ ДАННЫХ! ' + str(e))
        for url in self.urls.items():
            print(url)
            try:
                connection = sql.connect('wildberries.db')
                with connection:
                    cursor = connection.cursor()
                    cursor.execute('INSERT INTO urls values (?,?,?)', tuple([url[0], url[1][0], url[1][1]]))
                    connection.commit()
            except Exception as e:
                self.log('НЕ УДАЛОСЬ ЗАПИСАТЬ В БАЗУ ДАННЫХ! ' + str(e))
        self.products = dict()
        self.urls = dict()

    def reopen_browser(self):
        url = self.driver.current_url
        self.driver.quit()
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("general.useragent.override", self.user_agent_s.get_random_user_agent())
        self.driver = webdriver.Firefox(options=self.options, firefox_profile=self.profile)
        self.log('------------------------------------------------------------------------------------------------')
        self.log("CURRENT URL ON REOPEN: " + str(url))
        self.log('------------------------------------------------------------------------------------------------')
        self.driver.get(url)
        yield Request(
            url=url,
            callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "goods-card__container"))
            )
        except Exception as e:
            self.log(str(e))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        cards = soup.findAll('li', {'class':'goods__item'})
        self.log(str(cards))
        if cards is None or len(cards) < 1:
            cards = self.check_condition_cards(soup)
            if cards is None or len(cards) < 1:
                self.log('------------------------------------------------------------------------------------------------')
                self.log('Card object is None')
                self.log('------------------------------------------------------------------------------------------------')
                self.log(self.driver.execute_script("return navigator.userAgent;"))
                self.log('------------------------------------------------------------------------------------------------')
                self.log("URL :" + str(self.driver.current_url))
                self.log('------------------------------------------------------------------------------------------------')
                # self.log(str(cards))
                self.log('------------------------------------------------------------------------------------------------')
                # test
                with open(str(self.driver.current_url.split('//')[1].split('/')[0])+'.html', 'wb') as f:
                    f.write(self.driver.page_source.encode())
                # end test
                self.check_detected_scraping(soup)
        for card in cards:
            product_name = card.find('p', {'class': 'goods-card__description'})
            product_price = card.find('span', {'class': 'goods-card__price'})
            if card.find('span', {'class': 'goods-goods-card__price-now'}) is not None:
                product_price = card.find('span', {'class': 'goods-goods-card__price-now'})
            if product_name is not None:
                print(product_name)
                product_name = card.find('p', {'class': 'goods-card__description'}).text
            if product_price is not None:
                product_price = card.find('span', {'class': 'goods-card__price'}).text
            if product_name is None or product_price is None:
                product_name, product_price = self.check_condition_products(soup, card)
            self.log(str(product_name) + str(product_price))
            if product_name is None or product_price is None:
                self.log('No find product name or product price!')
            else:
                self.log("PRODUCT NAME: " + str(product_name))
                self.log("PRODUCT PRICE: " + str(product_price))
                # self.log(type(product_name))
                # self.log(type(product_price))
                # self.log("OUT: " + str(type(product_name)) + ' ' + str(type(product_price)) + ' ' + str(type(self.products)))
                if isinstance(product_name, str) or isinstance(product_price, str):
                    name = product_name.replace('\n', '')
                    price = product_price.replace('\u00A0', '')
                else:
                    name = product_name.text.replace('\n', '')
                    price = product_price.text.replace('\u00A0', '')
                self.products[name.replace(' / ', ' ')] = price.replace('₽', '')
        self.log('PRODUCTS: ' + str(self.products))
        if self.products is None or len(self.products) < 1:
            self.log('------------------------------------------------------------------------------------------------')
            self.log('PRODUCTS IS NULL !')
            self.log('------------------------------------------------------------------------------------------------')
            self.log("URL: " + str(self.driver.current_url))
            self.log('------------------------------------------------------------------------------------------------')
            self.log("CARDS BODY: " + str(cards))
            self.urls[self.driver.current_url] = [hashlib.md5(self.driver.page_source.encode()).hexdigest().__str__(), True]
            self.log(self.driver.execute_script("return navigator.userAgent;"))
            # self.reopen_browser()
        else:
            self.urls[self.driver.current_url] = [hashlib.md5(self.driver.page_source.encode()).hexdigest().__str__(), False]

        next_page = [i.get('href').__str__() for i in soup.findAll('a') if i.get('href').__str__() not in self.visited]
        while next_page:
            page = next_page.pop(0)
            if page not in self.visited:
                self.visited.append(page)
                self.write_db()
                if page[0] == '/':
                    page = 'https://www.wildberries.ru' + page
                    if 'wildberries.ru' in page:
                        next_page.append(response.urljoin(page))
                        yield Request(page, callback=self.parse)


