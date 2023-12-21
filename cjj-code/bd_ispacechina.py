import os
# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys
sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
from selenium.webdriver.common.by import By
import jionlp
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S
from selenium import webdriver
import platform

plat = platform.system().lower()


def process_expression(expression):
    global result
    pattern = r"(\d+)([+\-*\/x])(\?=)(\d+)"
    matches = re.search(pattern, expression)

    if matches:
        num1 = int(matches.group(1))
        operator = matches.group(2)
        num2 = int(matches.group(4))
        try:
            num3 = int(matches.group(5))

            num2 = int(str(num2) + str(num3))
        except Exception as e:
            pass

        if operator == '+':
            result = num2 - num1
        elif operator == '-':
            result = num2 + num1
        elif operator == 'x':
            result = num2 // num1
        elif operator == '/':
            result = num2 * num1

        return result

    return "Invalid expression"


def process_expression(expression):
    pattern = r"(\d+)([+\-*\/×])(\?=)(\d+)"
    matches = re.search(pattern, expression)

    if matches:
        num1 = int(matches.group(1))
        operator = matches.group(2)
        num2 = int(matches.group(4))
        try:
            num3 = int(matches.group(5))

            num2 = int(str(num2) + str(num3))
        except Exception as e:
            pass

        if operator == '+':
            result = num2 - num1
        elif operator == '-':
            result = num2 + num1
        elif operator == 'x':
            result = num2 // num1
        elif operator == '/':
            result = num2 * num1

        return result

    return "Invalid expression"


def handle_code():
    import requests
    import base64

    '''
    通用文字识别（高精度版）
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open('cropped_screenshot.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '24.325c5bfa097d6039737ab63c65bcedcd.2592000.1696782894.282335-38507260'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print(response.json())
        return response.json()["words_result"][0]["words"]


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "bd_ispacechina"

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
            #chrome_options.add_argument("--headless=new")  # 无界面
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option('excludeSwitches',
                                                   ['enable-automation'])
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            prefs = {"profile.managed_default_content_settings.images": 2}
            #chrome_options.add_experimental_option("prefs", prefs)
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

        return self.get_selenium_obj(url=url)

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

        list = driver.find_elements(By.XPATH, '//*[@id="gform"]/div/div/div[2]/div[6]/div')

        auction_infos = []
        for i in list:
            # 网站原始id
            # origin_id: str
            origin_id = i.get_attribute('probid')

            # 拍卖标的ID
            # auction_id: str
            auction_id = f"{self.website}_{origin_id}"

            # 拍卖公告名称
            # assets_name: str
            try:
                assets_name = i.find_element(By.XPATH, './/div[1]/h2').text
            except Exception as e:
                continue

            # 报名开始时间
            # announcement_start_time: str
            try:
                announcement_start_time = i.find_element(By.XPATH, './/div[1]/ul/li[3]').text
                announcement_start_time = str_to_y_m_d_H_M_S(jionlp.parse_time(announcement_start_time)["time"][0])
            except Exception as e:
                continue

            # 报名截止时间
            # announcement_end_time: str
            try:
                announcement_end_time = i.find_element(By.XPATH, './/div[1]/ul/li[4]').text
                announcement_end_time = str_to_y_m_d_H_M_S(jionlp.parse_time(announcement_end_time)["time"][0])
            except Exception as e:
                continue

            # 状态
            # state: str
            state = "正在招标中"

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
            b = jionlp.parse_location(assets_name)
            province = b.get("province")
            if not province:
                province = "四川省"

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

            # 拍卖链接
            # url: str
            url = f"https://bd.ispacechina.com/exp/bidding/sell/signup/toZbggInfoHt.do?probid={origin_id}"


            if self.mysql_query(assets_name=auction_title, announcement_end_time=str_to_y_m_d_H_M_S(announcement_end_time)):
                print("跳过")
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

        details = driver.find_element(By.XPATH, '//*[@id="gform"]/div[2]/div[3]').get_attribute("outerHTML").replace(
            " ",
            "").replace(
            "\n", "").replace("\t", "")

        return auction_info, Auction_Detials(
            state=auction_info.state,
            url=auction_info.url,
            detials=details
        )

    # 启动函数
    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 20  # 写死20

        username = "Yanghao199081"
        passwprd = "yanghao199081"

        urls = [
            "https://bs.ispacechina.com/login/bdIndex.do",
            'https://bd.ispacechina.com/retrieve.do',
        ]

        logtool.info("开始")

        # 请求列表页
        driver = self.data_list(url=urls[0])

        # 处理登录
        driver.find_element(By.XPATH, '//*[@id="commonLogin"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="gform"]/div[1]/div[1]/span/div/p').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="bcodes"]/li[2]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="uid"]').send_keys(username)
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="kl"]').send_keys(passwprd)

        # 处理验证码
        element = driver.find_element(By.XPATH, '//*[@id="img_rand_code"]')
        element_location = element.location
        element_size = element.size

        driver.save_screenshot("screenshot1.png")
  
        from PIL import Image

        # 获取整个网页的截图
        driver.save_screenshot("screenshot.png")

        # 打开截图
        screenshot = Image.open("screenshot.png")

        # 裁剪指定区域
        left = element_location['x']
        top = element_location['y']
        right = element_location['x'] + element_size['width']
        bottom = element_location['y'] + element_size['height']
        cropped_image = screenshot.crop((left, top, right, bottom))

        # 保存裁剪后的截图
        cropped_image.save("cropped_screenshot.png")

        # 处理验证码
        code = handle_code()
        print(code)
        result = process_expression(str(code))

        if result == "Invalid expression":
            print("验证码错误")
            return

        time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="randCode"]').send_keys(result)
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="gform"]/div[1]/button').click()

        time.sleep(5)

        # 请求列表页
        driver = self.data_list(url=urls[1])

        while minpage < maxpage:

            time.sleep(5)
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

            minpage += 1

            # 请求列表页
            driver = self.data_list(url=urls[1])
            driver.find_element(By.XPATH, '//*[@id="pageno"]').clear()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="pageno"]').send_keys(minpage)
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="sure"]').click()

        self.quit_driver()


if __name__ == '__main__':
    wk = Wk()
    wk.action()
