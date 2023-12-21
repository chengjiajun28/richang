import json
import platform
import time
from abc import ABC, abstractmethod

import pymysql
from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from selenium import webdriver

from ruseinfo.auction import logtool
from ruseinfo.mongodb_config import Mongo

plat = platform.system().lower()


class BaseCrawler(ABC):
    def __init__(self, auction_info_table_name="auctionInfo", auction_detail_table_name="auctionDetail"):
        self.mongo = Mongo("duoybdb_prd")
        # self.mongo = Mongo("duoybdb_uat")
        self.auction_info_table_name = auction_info_table_name
        self.auction_detail_table_name = auction_detail_table_name
        # self.wuzishebei = "物资设备"
        # self.jidongche = "机动车"

        self.jixieshebei = "机械设备"
        self.jidongche = "机动车"
        self.feijiuwuzhi = "废旧物资"
        self.chaichu = "拆除"
        self.qita = "其它"

        self.driver = None

    def init_driver(self):
        if plat == 'windows':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        elif plat == 'linux':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")  # 无界面
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)

    # 将数据缓存到数据库中
    def cache_mysql_datas(self, website, datas):
        # 数据库连接配置
        config = {
            'host': '118.195.246.81',
            'port': 3406,
            'user': 'root',
            'password': 'ruse#@!2022r',
            'db': 'datas',
            'charset': 'utf8mb4'
        }

        # 连接到数据库
        connection = pymysql.connect(**config)

        try:
            # 使用cursor()方法创建一个游标对象，用于执行SQL语句
            with connection.cursor() as cursor:
                # 定义SQL查询语句
                sql = "INSERT INTO temporary_datas ( website, datas) VALUES ( %s,%s);"

                # 执行SQL查询
                cursor.execute(sql, (website, json.dumps(datas),))

                # 提交更改
                connection.commit()

        finally:
            # 关闭数据库连接
            connection.close()

    def delete_mysql_datas(self, id):
        # 数据库连接配置
        config = {
            'host': '118.195.246.81',
            'port': 3406,
            'user': 'root',
            'password': 'ruse#@!2022r',
            'db': 'datas',
            'charset': 'utf8mb4'
        }

        # 连接到数据库
        connection = pymysql.connect(**config)

        try:
            # 使用cursor()方法创建一个游标对象，用于执行SQL语句
            with connection.cursor() as cursor:
                # 定义SQL查询语句
                sql = f"DELETE FROM temporary_datas WHERE id = {id};"

                # 执行SQL查询
                cursor.execute(sql, )

                # 提交更改
                connection.commit()

        finally:
            # 关闭数据库连接
            connection.close()

    def init_page(self):

        # do1 = ChromiumOptions().set_paths(local_port=random.randint(1, 9999))
        # page = ChromiumPage(addr_or_opts=do1)

        co1 = ChromiumOptions().auto_port()
        page = ChromiumPage(co1)

        return page

    def init_page_user(self):
        page = ChromiumPage()

        return page

    def get_page_user_obj(self, url, headers=None, cookies=None):
        # 创建浏览器对象
        page1 = self.init_page_user()

        if headers:
            page1.set.headers(headers=headers)

        if cookies:
            page1.set.cookies(cookies=cookies)

        page1.get(url=url, interval=3)  # 获取网页

        return page1

    def get_page_obj(self, url, headers=None, cookies=None):
        # 创建浏览器对象
        page1 = self.init_page()

        if headers:
            page1.set.headers(headers=headers)

        if cookies:
            page1.set.cookies(cookies=cookies)

        page1.get(url=url, interval=3)  # 获取网页

        return page1

    def get_selenium_obj(self, url):
        if not self.driver:
            self.init_driver()
        self.driver.get(url=url)  # 获取网页

        return self.driver

    def getHTMLText(self, url):
        if not self.driver:
            self.init_driver()
        self.driver.get(url)  # 获取网页
        time.sleep(2)
        html_page = self.driver.page_source
        return html_page

    def getHTMLTextRefresh(self, url):
        if not self.driver:
            self.init_driver()
        self.driver.get(url)  # 获取网页
        self.driver.get(url)  # 获取网页
        # print(self.driver.get(url))
        time.sleep(2)
        html_page = self.driver.page_source
        return html_page

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    @abstractmethod
    def data_list(self, *args, **kwargs):
        pass

    @abstractmethod
    def data_details(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_total_page(self, *args, **kwargs):
        pass

    @abstractmethod
    def parse_data_list(self, *args, **kwargs):
        pass

    @abstractmethod
    def parse_data_details(self, *args, **kwargs):
        pass

    def get_n(self, lists, n):
        return lists[n] if lists and isinstance(lists, list) and len(lists) >= n + 1 else None

    def insert_many_auction_info(self, data):
        return self.mongo.insert_many(self.auction_info_table_name, data)

    def insert_many_auction_detail(self, data):
        return self.mongo.insert_many(self.auction_detail_table_name, data)

    def insert_one_auction_detail(self, data):
        return self.mongo.insert_one(self.auction_detail_table_name, data)

    def insert_one_auction_info(self, data):
        return self.mongo.insert_one(self.auction_info_table_name, data)

    def exist_by_aution_id(self, auctionId):
        dataList = self.mongo.find(self.auction_info_table_name, {"auctionId": auctionId})
        return len(dataList) > 0

    def query_by_auction_id(self, auctionId):
        dataList = self.mongo.find(self.auction_info_table_name, {"auctionId": auctionId})
        return dataList

    def exist_by_aution_name(self, name):
        dataList = self.mongo.find(self.auction_info_table_name, {"assetsName": name})
        return dataList

    def mysql_query(self, *args, **kwargs):
        result = False
        connection = pymysql.connect(
            host='118.195.246.81',
            port=3406,
            user='root',
            password='ruse#@!2022r',
            database='ruseinfo_uat',
        )

        cursor = connection.cursor()

        assets_name = kwargs.get("assets_name")

        if kwargs.get("announcement_start_time"):
            announcement_start_time = kwargs.get("announcement_start_time")

            try:
                # 执行查询语句
                sql = f"SELECT * FROM auction_info WHERE assets_name = '{assets_name}' AND DATE(announcement_start_time) = DATE('{announcement_start_time}')"
                cursor.execute(sql)
                result = cursor.fetchall()

            except Exception as e:
                cursor.close()
                connection.close()

        if kwargs.get("announcement_end_time"):
            announcement_end_time = kwargs.get("announcement_end_time")

            try:
                # 执行查询语句
                sql = f"SELECT * FROM auction_info WHERE assets_name = '{assets_name}' AND DATE(announcement_end_time) = DATE('{announcement_end_time}')"

                cursor.execute(sql)
                result = cursor.fetchall()

            except Exception as e:
                cursor.close()
                connection.close()

        if result:
            return True

        return result

    def select_mysql_datas(self, database_name, table_name):
        # 数据库连接配置
        config = {
            'host': '118.195.246.81',
            'port': 3406,
            'user': 'root',
            'password': 'ruse#@!2022r',
            'db': f'{database_name}',
            'charset': 'utf8mb4'
        }

        # 连接到数据库
        connection = pymysql.connect(**config)

        try:
            # 使用cursor()方法创建一个游标对象，用于执行SQL语句
            with connection.cursor() as cursor:
                # 定义SQL查询语句
                sql = f"SELECT * FROM {table_name}"

                # 执行SQL查询
                cursor.execute(sql)

                # 使用fetchall()方法获取所有数据
                rows = cursor.fetchall()

                datas = []
                # 遍历结果集，将每行数据转换为字典，并打印字段名和对应的值
                for row in rows:
                    data_dict = dict(zip([column[0] for column in cursor.description], row))

                    datas.append(data_dict)

        finally:
            # 关闭数据库连接
            connection.close()

        return datas

    def select_mysql_classification(*args, **kwargs):
        connection = pymysql.connect(
            host='118.195.246.81',
            port=3406,
            user='root',
            password='ruse#@!2022r',
            database='datas',
        )

        cursor = connection.cursor()

        sql = f"SELECT * FROM categories"
        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        connection.close()

        classification = {}
        for words_list in result:
            # 使用 split 方法将字符串分割，以逗号为分隔符
            words_lists = str(words_list[1]).split(',')

            # 使用 strip 方法移除元素中的逗号和空格
            words_lists = [word.strip('，') for word in words_lists]

            # 使用 filter 函数过滤掉空字符串，并将结果转换为列表
            words_lists = list(filter(lambda x: x != '', words_lists))

            # 移除列表中的空格
            words_lists = [word for word in words_lists if word != '']

            classification.update({
                words_list[0]: words_lists
            })

        return result

    # def delete_one_auction_detail(self,id):
    #     self.mongo.delete(self.auction_detail_table_name,condition="id={0}".format(id))
    #
    # def delete_many_auction_info(self,id):
    #     self.mongo.delete(self.auction_detail_table_name,condition="id={0}".format(id))
    def format_html(self, html_str):
        if not html_str:
            return ""
        move = dict.fromkeys((ord(c)) for c in u"\xa0\t\n\r")
        return html_str.translate(move)  # 就是不翻译这几个标签

    def process(self, needDriver=True, *args, **kwargs):
        try:
            if needDriver:
                self.init_driver()
            self.action(*args, **kwargs)
        except Exception as error:
            logtool.error("error {0}".format(error))
        finally:
            self.quit_driver()

    @abstractmethod
    def action(self, *args, **kwargs):
        pass
        # pageIndex = 1
        # totalpage = 1
        # while True:
        #     list_response = self.data_list(pageIndex)
        #     if pageIndex == 1:
        #         totalpage = int(self.get_total_page(list_response))
        #         logtool.info("------dscq totalpage " + str(totalpage) + "------")
        #     if pageIndex > totalpage:
        #         return
        #     logtool.info("------dscq page: " + str(pageIndex) + " parse start------")
        #     auctions = self.parse_data_list(list_response)
        #     logtool.info("------dscq page: " + str(pageIndex) + " parse end------")
        #     for auction in auctions:
        #         logtool.info("------dscq details for id: " + auction.origin_id + " start------")
        #         details_response = self.data_details(auction.origin_id)
        #         logtool.info("------dscq details for id: " + auction.origin_id + " end------")
        #         logtool.info("------dscq details for id: " + auction.origin_id + " parse start------")
        #         self.parse_data_details(details_response, auction)
        #         logtool.info("------dscq details for id: " + auction.origin_id + " parse end------")
        #     pageIndex = pageIndex + 1
