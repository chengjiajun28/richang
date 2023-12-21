import os

# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
import datetime
from urllib.parse import unquote

import requests
from selenium.webdriver.common.by import By
import jionlp
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S
from selenium import webdriver
import platform

plat = platform.system().lower()


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'JSESSIONID=b3f238ff7f3b2f7b6bfa02a50cb7; insert_cookie=82956849',
            'DNT': '1',
            'Origin': 'http://deal.ggzy.gov.cn',
            'Referer': 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

        self.website = "ggzy_gov"

    def init_driver(self):
        if plat == 'windows':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option('excludeSwitches',
                                                   ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_window_size(1920, 1080)
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                       Object.defineProperty(navigator, 'webdriver', {
                       get: () => undefined
                       })
                   """
            })
        elif plat == 'linux':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")  # 无界面
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option('excludeSwitches',
                                                   ['enable-automation'])
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
            self.driver.set_window_size(1920, 1080)
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                               Object.defineProperty(navigator, 'webdriver', {
                               get: () => undefined
                               })
                           """
            })

    # 请求列表页
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        type = kwargs.get("type")
        page = kwargs.get("page")

        date = datetime.date.today()
        from datetime import timedelta
        # 获取当前日期和时间
        now = datetime.datetime.now()

        # 将日期改为10号
        new_date = now.today().replace(day=10)
        new_date = new_date.strftime("%Y-%m-%d")

        data = {
            'TIMEBEGIN_SHOW': str(new_date),
            'TIMEEND_SHOW': str(date),
            'TIMEBEGIN': str(new_date),
            'TIMEEND': str(date),
            'SOURCE_TYPE': '1',
            'DEAL_TIME': '02',
            'DEAL_CLASSIFY': '01',
            'DEAL_STAGE': '0101',
            'DEAL_PROVINCE': '0',
            'DEAL_CITY': '0',
            'DEAL_PLATFORM': '0',
            'BID_PLATFORM': '0',
            'DEAL_TRADE': '0',
            'isShowAll': '1',
            'PAGENUMBER': page,
            'FINDTXT': type,
        }

        res = self.session.post(url=url, data=data)

        return res.json()

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表页
    def parse_data_list(self, *args, **kwargs):
        time.sleep(3)
        list_datas = kwargs.get("list_datas")

        auction_infos = []
        for i in list_datas:
            # 网站原始id
            # origin_id: str
            origin_id = i["url"].split("/")
            match = re.search(r"(.*?).shtml", origin_id[-1])
            if match:
                origin_id = match.group(1)

            # 拍卖标的ID
            # auction_id: str
            auction_id = f"{self.website}_{origin_id}"

            # 拍卖公告名称
            # assets_name: str
            assets_name = i["title"]

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = str_to_y_m_d_H_M_S(i["timeShow"])

            # 报名截止时间
            # announcement_end_time: str

            # 保证金
            # deposit: str

            # 图片url
            # img_url: str

            # imgPaths前缀
            # img_prefix: str

            # 图片路径，多个分隔
            # img_paths: str

            # 省份
            # province: str
            province = i['districtShow']

            # 城市
            # city: str
            # 县
            # county: str
            # 拍卖网站 标识符 可以是域名
            # website: str
            # 拍卖类型
            # assets_type: str
            assets_type = ""
            if "车" in assets_name:
                assets_type = self.jidongche
            else:
                assets_type = self.wuzishebei

            # 关注数
            # onlookers: str

            # 状态
            # state: str

            # 拍卖链接
            # url: str
            url = i["url"]

            if self.mysql_query(assets_name=auction_title, announcement_end_time=str_to_y_m_d_H_M_S(announcement_end_time)):
                print("跳过")
                continue


            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                announcement_start_time=announcement_start_time,
                # announcement_end_time=announcement_end_time,
                province=province,
                website=self.website,
                # state=state,
                url=url,
                assets_type=assets_type
            )

            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(3)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        url = driver.find_element(By.XPATH, '//*[@id="iframe0101"]').get_attribute('src')

        time.sleep(3)
        driver = self.data_details(url=url)
        time.sleep(3)

        return auction_info, Auction_Detials(
            state=auction_info.state,
            url=auction_info.url,
            detials=driver.find_element(By.XPATH, '/html/body/div').get_attribute("outerHTML")
        )

        # 启动函数

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 2  # 写死20

        urls = [
            "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp",
        ]

        types = ["废", "钢", "拆除"]

        logtool.info("开始")

        for type in types:

            while minpage < maxpage:

                # 请求列表页
                list_datas = self.data_list(url=urls[0], type=type, page=minpage)

                # 解析列表页
                auction_infos = self.parse_data_list(list_datas=list_datas["data"])

                for auction_info in auction_infos:
                    driver = self.data_details(url=auction_info.url)
                    auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

                    id = self.insert_one_auction_info(auction_info.to_json())
                    auction_detial.id = id
                    self.insert_one_auction_detail(auction_detial.to_json())

                    print(auction_info)
                    print(auction_detial)

                minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
