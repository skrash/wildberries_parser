# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sqlite3 as sql
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from random_user_agent.params import SoftwareName, OperatingSystem
import os


class WildberriesPipeline:

    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        # USER AGENT OPTIONS
        spider.software_names = [SoftwareName.FIREFOX.value]
        spider.operating_systems = [OperatingSystem.WINDOWS.value]
        spider.user_agent_s = UserAgent(software_names=spider.software_names, operating_systems=spider.operating_systems, limit=100)
        # FIREFOX OPTIONS
        spider.profile = FirefoxProfile(os.curdir + "\\Browser\\TorBrowser\\Data\\Browser\\profile.default")
        spider.binary = FirefoxBinary(os.curdir + "\\Browser\\firefox.exe")
        spider.torexe = os.popen(os.curdir + "\\Browser\\TorBrowser\\Tor\\tor.exe")
        spider.profile.set_preference('network.proxy.type', 1)
        spider.profile.set_preference('network.proxy.socks', '127.0.0.1')
        spider.profile.set_preference('network.proxy.socks_port', 9050)
        spider.profile.set_preference("network.proxy.socks_remote_dns", False)
        spider.options = Options()
        spider.options.headless = True
        spider.profile.set_preference("general.useragent.override", spider.user_agent_s.get_random_user_agent())
        spider.driver = webdriver.Firefox(options=spider.options, firefox_profile=spider.profile)

        try:
            connection = sql.connect('wildberries.db')
            with connection:
                cursor = connection.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS products (name VARCHAR(50) UNIQUE PRIMARY KEY, price INTEGER)')
                connection.commit()
                cursor.execute('CREATE TABLE IF NOT EXISTS urls (url VARCHAR(50) UNIQUE PRIMARY KEY,'
                               ' hash VARCHAR(25), is_banned BOOLEAN)')
                connection.commit()
        except Exception as e:
            spider.log('НЕ УДАЛОСЬ СОЗДАТЬ БАЗУ ДАННЫХ! ' + e.__str__())

    def close_spider(self, spider):
        spider.driver.quit()



