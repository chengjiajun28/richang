import re
import time

from lxml import etree
from selenium.webdriver.common.by import By
import os
# 文件目录
abs_path = os.path.abspath(__file__)
#print(abs_path[0:abs_path.find('auction')-1])
import sys
sys.path.append(abs_path[0:abs_path.find('auction')-1])
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
import requests

from tools import str_to_y_m_d_H_M_S
from selenium import webdriver
# coding=utf-8
import re
import sys
import json
import base64

import platform

plat = platform.system().lower()


# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
# else:
#     import urllib2
#     from urllib import quote_plus
#     from urllib2 import urlopen
#     from urllib2 import Request
#     from urllib2 import URLError
#     from urllib import urlencode

# 防止https证书校验不正确
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'wc6Gc1Ckzz0v3Ylo2dz7BMMc'

SECRET_KEY = 'oQfZtGnrbUgNK48fnUyoyMRp5swhVvbE'

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

"""
    获取token
"""


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    读取文件
"""


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""


def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)


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
        elif operator == '×':
            result = num2 // num1
        elif operator == '/':
            result = num2 * num1

        return result

    return "Invalid expression"


def main():
    # 获取access token

    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    text = ""

    # 读取测试图片
    file_content = read_file('image.jpg')

    # 调用文字识别服务
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

    # 解析返回结果
    result_json = json.loads(result)
    for words_result in result_json["words_result"]:
        text = text + words_result["words"]

    # 打印文字
    print(text)

    import re

    value = ""
    match = re.search(r"验证码：(.+?)看不清", text)
    if match:
        value = match.group(1)

    print(value)

    return process_expression(value)


def save_image_from_url(url, filename):
    import requests

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'yang199081=success; JSESSIONID=7F1641BD7CAFAF4D7BDED25EC67BD2BB.node1',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url=url,
                            headers=headers)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("图片保存成功")
    else:
        print(f"请求图片失败，状态码：{response.status_code}")


from PIL import Image


def crop_image(image_path, left, top, right, bottom, cropped_path):
    # 打开原始图片
    image = Image.open(image_path)

    # 裁剪指定位置的图片
    cropped_image = image.crop((left, top, right, bottom))

    # 保存裁剪后的图片
    cropped_image.save(cropped_path)


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "wm_norincogroup_ebuy"
        # self.wuzishebei = "物资设备"
        # self.che = "机动车"



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
          # chrome_options.add_experimental_option("prefs", prefs)
          self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)

    # 列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.getHTMLText(url)

    # 请求详情页
    def data_details(self, *args, **kwargs):
        driver = kwargs.get("driver")
        url = kwargs.get("url")

        return driver.get(url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        driver = kwargs.get("driver")

        list = driver.find_elements(By.XPATH, '/html/body/div[8]/div/div/div[2]/div[2]/div[1]/ul/li')

        auction_infos = []
        for i in list:
            onclick_value = i.get_attribute('onclick')
            start_index = onclick_value.find("'") + 1  # 获取第一个单引号的位置加1
            end_index = onclick_value.find("'", start_index)  # 获取第二个单引号的位置
            origin_id = onclick_value[start_index:end_index]  # 使用切片获取子字符串

            assets_name = i.find_element(By.XPATH, './/dl/dt').text

            announcement_start_time = i.find_element(By.XPATH, './/dl/dd[2]/em').text
            img_url = i.find_element(By.XPATH, './/img').get_attribute("src")
            province = i.find_element(By.XPATH, './/dl/dd[3]/em').text
            state = i.find_element(By.XPATH, './/i').text

            name_type = ""
            if "车" in assets_name:
                name_type = self.jidongche
            else:
                name_type = self.wuzishebei

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id="{0}_{1}".format(self.website, origin_id),
                assets_name=assets_name,
                announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
                img_url=img_url,
                province=province,
                website=self.website,
                state=state,
                assets_type=name_type
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        driver = kwargs.get("driver")
        url = kwargs.get("url")
        auction_info = kwargs.get("auction_info")

        time.sleep(5)

        announcement_end_time = driver.find_element(By.XPATH,
                                                    '/html/body/div[4]/div/div[2]/div[2]/div[2]/div[2]/div[2]/p[2]/span').text
      
        start_time, end_time = announcement_end_time.split("至")
        auction_info.announcement_end_time = str_to_y_m_d_H_M_S(end_time)

        deposit = driver.find_element(By.XPATH,
                                      '/html/body/div[4]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/ul/li[1]/p[1]/em').text
        auction_info.deposit = deposit

        images = driver.find_elements(By.XPATH,
                                      '//*[@id="focus_smaillPic_list"]/li')
        image_list = ""
        for image in images:
            image_str = image.find_element(By.XPATH, './/img').get_attribute('src')

            image_list += image_str + ";"

        auction_info.img_paths = image_list

        # onlookers = driver.find_element(By.XPATH,
        #                                 '/html/body/div[4]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/ul/li[3]/p[2]/em').text
        # auction_info.onlookers = onlookers

        datas = driver.find_elements(By.XPATH,
                                     '//*[@id="record"]/div[1]/ul/li')
        datas1 = driver.find_elements(By.XPATH,
                                      '//*[@id="record"]/div[2]/div/div')

        details = []
        n = 2
        for data in datas:
            data_dict = {}
            title = data.find_element(By.XPATH, '.').text

            datas1[n].get_attribute("outerHTML")

            data_dict["title"] = title
            data_dict["content"] = datas1[n].get_attribute("outerHTML").replace(" ", "").replace("\n", "")

            details.append(data_dict)

            n += 1

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=url, detials=details)

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 20  # 写死20

        username = 'yang199081'
        passwd = 'Yanghao199081@'

        #logtool.info("开始爬取")

        #logtool.info("获取列表")
        url = 'https://bs.norincogroup-ebuy.com/login/wsIndex.do'
        driver = self.get_selenium_obj(url=url)
        time.sleep(5)
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/h2/span[2]').click()

        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="uid"]').send_keys(username)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="kl"]').send_keys(passwd)
        time.sleep(3)

        # 截取图片
        driver.save_screenshot("image.jpg")

        crop_image(image_path="image.jpg", left=1000,
                   top=478,
                   right=1058,
                   bottom=503,
                   cropped_path="haha.png")

        code = main()
        driver.find_element(By.XPATH, '//*[@id="randCode"]').send_keys(code)

        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="loginBt"]').click()

        while maxpage >= minpage:

            time.sleep(3)

            # 解析列表页
            auction_infos = self.parse_data_list(driver=driver)

            for auction_info in auction_infos:
                url = f"https://wm.norincogroup-ebuy.com/exp/auction/buy/bout/seeBout.do?boutid={auction_info.origin_id}"

                auction_info.url = url

                # 请求详情页
                driver.get(url=url)

                # 解析详情页
                auction_info, auction_datails = self.parse_data_details(driver=driver, url=url,
                                                                        auction_info=auction_info)

                print(auction_info)

                id = self.insert_one_auction_info(auction_info.to_json())

                auction_datails.id = id

                self.insert_one_auction_detail(auction_datails.to_json())

            minpage += 1
            url1 = "https://wm.norincogroup-ebuy.com/index.do"
            driver = self.get_selenium_obj(url=url1)
            driver.find_element(By.XPATH, '//*[@id="pageno"]').clear()
            driver.find_element(By.XPATH, '//*[@id="pageno"]').send_keys(minpage)
            driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[2]/div[3]/div[2]/ul/div[2]/span[4]/a').click()

        driver.quit()


if __name__ == '__main__':
    wk = Wk()
    wk.action()
