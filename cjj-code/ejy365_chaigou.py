import os

# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])


import re
import time

import jionlp
from lxml import etree
from selenium.webdriver.common.by import By

import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
import requests

from tools import str_to_y_m_d_H_M_S


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Referer': 'http://www.wypai.net/bidlista0b1c0d1.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }
        self.session.headers.update(headers)
        self.website = "ejy365_chaigou"

    # 列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.getHTMLText(url)

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        html = kwargs.get("html")

        tree = etree.HTML(html)

        # 使用XPath选择需要的div元素
        div_elements = tree.xpath('/html/body/div[7]/div[3]/div[1]/div/div/ul/li')

        # 网址
        auction_infos = []
        for div in div_elements:
            url = div.xpath('.//a/@href')
            assets_name = div.xpath('.//a/span[1]/h3/text()')
            announcement_end_time = div.xpath('.//a/span[5]/span/text()')[0]

            b = jionlp.parse_location(assets_name)
            province = b.get("province")
            if not province:
                province = "四川省"

            deposit = div.xpath('.//a/span[4]/span/text()')[0].split(".")[0].replace(",", "")

            state = div.xpath('.//a/span[1]/span/span[1]/em/text()')

            origin_id = url[0].split("/")[-1:]

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id[0],
                auction_id="{0}_{1}".format(self.website, origin_id[0]),
                assets_name=assets_name[0],
                announcement_end_time=str_to_y_m_d_H_M_S(announcement_end_time),
                province=province,
                website=self.website,
                state=state[0],
                url=url[0],
                deposit=deposit
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(3)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        data_list = driver.find_element(By.XPATH,
                                        '/html/body/div[6]/div/div[3]/div[1]/div[1]/div[3]/div').get_attribute(
            "outerHTML")

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=data_list)

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 2  # 写死20

        url = [
            "https://www.ejy365.com/purchase/list?morejg=0&status=1&orderType=default&gonggaoTitle=%2520%25E9%2592%25A2&page={}",
            # 钢
        ]

        logtool.info("开始爬取e交易")

        while maxpage >= minpage:
            url1 = url[0].format(minpage)
            res = self.data_list(url=url1)

            # 解析列表页
            auction_infos = self.parse_data_list(html=res)

            for auction_info in auction_infos:
                driver = self.data_details(url=auction_info.url, auction_info=auction_info)

                # 解析详情页
                auction_info, auction_datail = self.parse_data_details(driver=driver, auction_info=auction_info)

                id = self.insert_one_auction_info(auction_info.to_json())
                auction_datail.id = id
                self.insert_one_auction_detail(auction_datail.to_json())

                print(auction_info)
                print(auction_datail)


            if len(auction_infos):
                minpage = maxpage

            minpage += 1

        self.quit_driver()


if __name__ == '__main__':
    wk = Wk()
    wk.action()
