import os
# 文件目录
abs_path = os.path.abspath(__file__)
import sys
sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
from datetime import datetime
from urllib.parse import unquote

import requests
from selenium.webdriver.common.by import By
import jionlp
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Client-Id': 'gxcq',
            'Connection': 'keep-alive',
            # 'Content-Length': '0',
            # 'Cookie': 'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1694741028; Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1694741113',
            'DNT': '1',
            'Origin': 'http://www.gxcq.com.cn',
            'Referer': 'http://www.gxcq.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

        self.website = "gxcq"

    # 请求列表页
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        params = kwargs.get("params")

        res = self.session.post(url=url, params=params)

        return res.json()["data"]["records"]

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表页
    def parse_data_list(self, *args, **kwargs):
        global origin_id
        datas = kwargs.get("datas")

        auction_infos = []
        for i in datas:
            # 网站原始id
            # origin_id: str

            match = re.search(r"(.*?).shtml", i["detailsUrl"].split("/")[-1])
            if match:
                origin_id = match.group(1)

            origin_id = origin_id

            # 拍卖标的ID
            # auction_id: str
            auction_id = f"{self.website}_{origin_id}"

            # 拍卖公告名称
            # assets_name: str
            assets_name = i['assetsName']

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = str_to_y_m_d_H_M_S(i["announcementStartTime"])

            # 报名截止时间
            # announcement_end_time: str
            announcement_end_time = str_to_y_m_d_H_M_S(i["announcementEndTime"])

            specified_time = datetime.strptime(announcement_end_time, "%Y-%m-%d %H:%M:%S")

            # 获取当前时间
            current_time = datetime.now()

            # 判断当前时间是否大于指定时间
            if current_time > specified_time:
                continue

            # 保证金
            # deposit: str
            deposit = i["deposit"]

            # 图片url
            # img_url: str
            img_url = i["imgUrl"]

            # imgPaths前缀
            # img_prefix: str

            # 图片路径，多个分隔
            # img_paths: str

            # 省份
            # province: str
            province = i["province"]

            # 城市
            # city: str
            city = i["city"]

            # 县
            # county: str
            county = i["county"]

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
            onlookers = i["circuseeCount"]

            # 状态
            # state: str
            state = i["state"][0]

            # 拍卖链接
            # url: str
            url = i["detailsUrl"]

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
                assets_type=assets_type,
                onlookers=onlookers,
                city=city,
                county=county,
                img_url=img_url,
                deposit=deposit,
            )

            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        logtool.info("进入详情页")
        time.sleep(3)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        # 将页面滚动到底部
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        titles = driver.find_elements(By.XPATH, '/html/body/div[7]/div/div/div[3]/div[2]/div[1]/ul/li')
        contents = driver.find_elements(By.XPATH, '//*[@id="noticeContent"]/div')
        details = []
        for title, content in zip(titles, contents):
            driver.execute_script("arguments[0].click();", title)

            data = {
                "title": title.text,
                "content": content.get_attribute("outerHTML")
            }
            if title.text == "相关附件下载":
                continue

            details.append(data)

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
            "http://www.gxcq.com.cn/api/dscq-project/search/page",
        ]

        params = {
            'size': '8',
            'current': '1',
            'q': '',
            'orderBy': '',
            'order': '',
            'minPrice': '',
            'maxPrice': '',
            'assetsTypeParent': 'FJWZ',
            'assetsTypeLeaf': '',
            'associationId': '',
            'state': '1',
        }

        logtool.info("开始")

        # 请求列表页
        datas = self.data_list(url=urls[0], params=params)

        # 解析列表页
        auction_infos = self.parse_data_list(datas=datas)

        for auction_info in auction_infos:
            driver = self.data_details(url=auction_info.url)
            auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

            id = self.insert_one_auction_info(auction_info.to_json())
            auction_detial.id = id
            self.insert_one_auction_detail(auction_detial.to_json())



if __name__ == '__main__':
    wk = Wk()
    wk.action()
