import os

# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
from datetime import datetime
from urllib.parse import unquote
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

        self.website = "cspea"


    def init_driver(self):
        if plat == 'windows':
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless=new")
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
            # chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_window_size(1920, 1080)
        elif plat == 'linux':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://f146.kdltps.com:15818')
            chrome_options.add_argument("--headless=new")  # 无界面
            chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

            chrome_options.add_argument('--disable-dev-shm-usage')
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
            self.driver.set_window_size(1920, 1080)

    # 请求列表页
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url)

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表页
    def parse_data_list(self, *args, **kwargs):
        time.sleep(3)
        driver = kwargs.get("driver")

        list = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/main/div[1]/div[5]/div[1]/div')

        auction_infos = []
        for i in list:
            # 网站原始id
            # origin_id: str
            url = i.find_element(By.XPATH, './/div[1]/div[1]/a').get_attribute('href')
            origin_id = url.split("/")[-1]

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + "_" + origin_id

            # 拍卖公告名称
            # assets_name: str
            assets_name = i.find_element(By.XPATH, './/div[1]/div[1]/a/span').text

            times_str = i.find_element(By.XPATH, './/div[2]/div[2]/span[2]').text
            # 使用正则表达式匹配时间字符串
            pattern = r"\d{4}-\d{2}-\d{2}"
            matches = re.findall(pattern, times_str)

            # 转换时间字符串到指定格式
            start_time = datetime.strptime(matches[0] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(matches[1] + " 00:00:00", "%Y-%m-%d %H:%M:%S")

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = str_to_y_m_d_H_M_S(str(start_time))

            # 报名截止时间
            # announcement_end_time: str
            announcement_end_time = str_to_y_m_d_H_M_S(str(end_time))

            specified_time = datetime.strptime(announcement_end_time, "%Y-%m-%d %H:%M:%S")
            # 获取当前时间
            current_time = datetime.now()
            # 判断当前时间是否大于指定时间
            if current_time > specified_time:
                continue

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
            province = i.find_element(By.XPATH, 'div[2]/div[1]/span[2]').text
            b = jionlp.parse_location(province)
            province = b.get("province")

            # 城市
            # city: str
            # 县
            # county: str
            # 拍卖网站 标识符 可以是域名
            # website: str
            # 拍卖类型
            # assets_type: str
            # 关注数
            # onlookers: str
            # 状态
            # state: str
            state = "正在披露"

            # 拍卖链接
            # url: str
            url = url

            if self.mysql_query(assets_name=assets_name, announcement_start_time=announcement_start_time):
                continue

            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                announcement_start_time=announcement_start_time,
                announcement_end_time=announcement_end_time,
                province=province,
                website=self.website,
                state=state,
                url=url
            )

            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(3)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        images = driver.find_elements(By.XPATH,
                                      '//*[@id="root"]/div/div/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/table[5]/tbody/tr[1]/td/img')

        image_urls = ""
        for n, url in enumerate(images):
            a = url.get_attribute('src')
            if n == 0:
                auction_info.img_ur = a

            image_urls += ";" + a

        auction_info.img_paths = image_urls[1:]

        titles = driver.find_elements(By.XPATH,
                                      '//*[@id="course_container"]/div')

        contents = driver.find_elements(By.XPATH,
                                        '//*[@id="root"]/div/div/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/table')

        details = []
        for title, content in zip(titles, contents):
            title = title.text
            content = content.get_attribute("outerHTML").replace(" ", "").replace("\n", "").replace("\t", "")

            if title in ["图片及附件", "我要留言"]:
                continue

            a = {
                "title": title,
                "content": content
            }
            details.append(a)

        try:
            fujains = driver.find_elements(By.XPATH,
                                           '//*[@id="root"]/div/div/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/table[5]/tbody/tr[2]/td/a')

            for fujian in fujains:
                text = fujian.get_attribute('href').split("/")[-1]
                pattern = r"^(.+)\.pdf"
                pattern1 = r"^(.+)\.jpg"

                try:
                    match = re.match(pattern, text)
                except Exception as e:
                    match = re.search(pattern1, text)

                matched_data = ""
                if match:
                    matched_data = match.group(1)

                name = text
                url = fujian.get_attribute('href')

                b = [{
                    "title": "附件",
                    "content": [{
                        "title": unquote(matched_data),
                        "content": url
                    }]

                }]

                details.append(b)

        except Exception as e:
            pass

        print()

        return auction_info, Auction_Detials(
            state=auction_info.state,
            url=auction_info.url,
            detials=details
        )

    # 启动函数
    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 2  # 写死20

        urls = [
            "https://www.cspea.com.cn/list?c=C01&i=4&s=A02,A03",
            # "https://www.baidu.com",
        ]

        logtool.info("开始")

        # 请求列表页
        driver = self.data_list(url=str(urls[0]))
        time.sleep(3)
        logtool.info("开始")

        # 翻页
        # for i in range(maxpage):
        #     time.sleep(1)
        #     actions = ActionChains(driver)
        #     actions.send_keys(Keys.END).perform()
        #     time.sleep(3)

        # 解析列表页
        auction_infos = self.parse_data_list(driver=driver)

        for auction_info in auction_infos:
            driver = self.data_details(url=auction_info.url)

            auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)
            id = self.insert_one_auction_info(auction_info.to_json())
            auction_detial.id = id
            self.insert_one_auction_detail(auction_detial.to_json())

            print(auction_info)
            print(auction_detial)


if __name__ == '__main__':
    wk = Wk()
    wk.action()
