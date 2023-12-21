import os
# 文件目录
abs_path = os.path.abspath(__file__)
#print(abs_path[0:abs_path.find('auction')-1])
import sys
sys.path.append(abs_path[0:abs_path.find('auction')-1])

from selenium.webdriver.common.by import By
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S
import re
import time
from datetime import datetime
from selenium import webdriver
import logtool
import platform
from urllib.parse import unquote

plat = platform.system().lower()


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "cquae"

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

    # 列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        global origin_id
        time.sleep(3)
        driver = kwargs.get("driver")

        list = driver.find_elements(By.XPATH, '/html/body/div[6]/div[5]/div[2]/div')

        auction_infos = []
        for i in list:
            # 网站原始id
            # origin_id: str
            a = i.find_element(By.XPATH, './/a')
            url = a.get_attribute('href')

            pattern = r"\?id=(\d+)"
            try:
                matches = re.findall(pattern, url)
            except Exception as e:
                continue

            try:
                origin_id = matches[0]
            except Exception as e:
                continue

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + "_" + str(origin_id)

            # 拍卖公告名称
            # assets_name: str
            assets_name = i.find_element(By.XPATH, './/table/tbody/tr/td[2]/div[1]/div[1]').text

            pattern = r"\d{4}-\d{2}-\d{2}"
            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = i.find_element(By.XPATH, './/table/tbody/tr/td[3]/div[1]/span').text
            matches = re.findall(pattern, announcement_start_time)
            announcement_start_time = str_to_y_m_d_H_M_S(matches[0])

            # 报名截止时间
            # announcement_end_time: str
            announcement_end_time = i.find_element(By.XPATH, './/table/tbody/tr/td[3]/div[2]/span').text
            matches = re.findall(pattern, announcement_end_time)
            announcement_end_time = str_to_y_m_d_H_M_S(matches[0])

            specified_time = datetime.strptime(announcement_end_time, "%Y-%m-%d %H:%M:%S")

            # 获取当前时间
            current_time = datetime.now()

            # 判断当前时间是否大于指定时间
            if current_time > specified_time:
                continue

            # 保证金
            # deposit: str
            deposit = i.find_element(By.XPATH, './/table/tbody/tr/td[4]/div[2]/span[2]/b').text
            deposit = float(deposit) * 10000

            # 图片url
            # img_url: str
            img_url = i.find_element(By.XPATH, './/table/tbody/tr/td[1]/div/img').get_attribute('src')

            # imgPaths前缀
            # img_prefix: str
            # 图片路径，多个分隔
            # img_paths: str

            # 省份
            # province: str

            # 城市
            # city: str

            # 县
            # county: str
            # 拍卖网站 标识符 可以是域名
            # website: str
            # 拍卖类型
            # assets_type: str
            name_type = ""
            if "车" in assets_name:
                name_type = self.jidongche
            else:
                name_type = self.wuzishebei

            # 关注数
            # onlookers: str
            try:
                onlookers = int(i.find_element(By.XPATH, './/table/tbody/tr/td[2]/div[3]/div/span[2]').text)
            except Exception as e:
                onlookers = i.find_element(By.XPATH, './/table/tbody/tr/td[2]/div[3]/div/span[3]').text

            # 状态
            # state: str
            state = "网上报名"

            # 拍卖链接
            # url: str
            url = url

            # sync_uat: bool = False
            # sync_prd: bool = False

            if self.mysql_query(assets_name=auction_title, announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time)):
                print("跳过")
                continue

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                announcement_start_time=announcement_start_time,
                announcement_end_time=announcement_end_time,
                deposit=deposit,
                img_url=img_url,
                # province=province,
                onlookers=onlookers,
                state=state,
                url=url,
                website=self.website,
                assets_type=name_type
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        global haha
        time.sleep(3)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        diqu = driver.find_element(By.XPATH, '//*[@id="xmggs"]/table[1]/tbody/tr[4]/td[2]').text

        import jionlp

        b = jionlp.parse_location(diqu)

        # 省份
        # province: str
        auction_info.province = b["province"]

        # 城市
        # city: str
        auction_info.city = b["city"]

        # 县
        # # county: str
        # auction_info.province = df["县"].values

        list = driver.find_elements(By.XPATH, '/html/body/div[6]/div[2]/div[2]/div/div')
        list1 = driver.find_elements(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div')

        # 图片
        images = driver.find_elements(By.XPATH, '//*[@id="tpsps"]/div/div')
        image_urls = ""
        for image in images:
            # image.find_elements(By.XPATH, './/img').get_attribute('src')
            image_urls += ";" + image.find_element(By.XPATH, './/img').get_attribute('src')

        auction_info.img_paths = image_urls[1:]

        details = []
        for i in list:
            dict = {}
            id = i.get_attribute('id')
            title = i.text
            if title in ["图片视频", "资料下载", "地图位置"]:
                continue

            for i1 in list1:
                id1 = i1.get_attribute('id')
                if id + "s" == id1:
                    dict['title'] = title
                    dict["content"] = i1.get_attribute("outerHTML").replace(" ", "").replace("\n", "").replace("\t", "")

            details.append(dict)

        fujians = driver.find_elements(By.XPATH, '//*[@id="fjxzs"]/table/tbody/tr/td/a')

        annex = []
        for fujian in fujians:
            text = fujian.get_attribute('href').split("/")[-1]
            pattern = r"^(.+)\.pdf"
            pattern1 = r"^(.+)\.jpg"
            pattern2 = r"^(.+)\.png"

            try:
                match = re.match(pattern, text)
            except Exception as e:
                try:
                    match = re.search(pattern1, text)
                except Exception as e:
                    match = re.search(pattern2, text)

            matched_data = ""
            if match:
                matched_data = match.group(1)

            a = {
                "title": unquote(matched_data),
                "url": fujian.get_attribute('href')
            }
            annex.append(a)

        if annex:
            a = {
                "title": "附件",
                "content": annex
            }
            details.append(a)

        details = [item for item in details if item]

        return auction_info, Auction_Detials(
            state=auction_info.state,
            url=auction_info.url,
            detials=details
        )

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 20  # 写死20

        urls = [
            "https://www.cquae.com/Project?q=s&projectID=3&type=8&priceID=8&page={0}",
            "https://www.cquae.com/Project?q=s&projectID=3&type=7&priceID=9&page={0}"
        ]

        for url in urls:
            logtool.info("开始爬取")
            logtool.info("获取列表")

            while minpage < maxpage:
                url1 = url.format(minpage)
                driver = self.data_list(url=url1)
                auction_infos = self.parse_data_list(driver=driver)

                for auction_info in auction_infos:
                    driver = self.data_details(url=auction_info.url)
                    auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

                    id = self.insert_one_auction_info(auction_info.to_json())
                    auction_detial.id = id
                    self.insert_one_auction_detail(auction_detial.to_json())
                    # print(auction_info)
                    # print(auction_detial)

              minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
