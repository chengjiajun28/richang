import os

# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
from lxml import etree
from selenium.webdriver.common.by import By
import logtool
from tools import str_to_y_m_d_H_M_S
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
import requests


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
        self.website = "wypai"

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
        div_elements = tree.xpath('//*[@id="form1"]/div[4]/div')

        # 网址
        auction_infos = []
        for div in div_elements:
            id = div.xpath('.//div[@class="tu"]/a/@href')
            assets_name = div.xpath('.//div[@class="name_div"]/div[1]/a/text()')
            announcement_start_time = div.xpath('.//div[@class="state"]/div[2]/text()')
            image_url = div.xpath('.//div[@class="tu"]/a/img/@src')
            province = div.xpath('.//div[@class="xinxi"]/span[4]/text()')
            website = "wypai"
            state = div.xpath('.//div[@class="state"]/div[1]/text()')

            url = "http:" + id[0]

            print(id[0])

            match = re.search(r"laddershow_(.*?).html", id[0])
            origin_id = ""
            if match:
                origin_id = match.group(1)

            # 解析时间
            datetime_str = announcement_start_time[0]
            datetime_str = datetime_str.replace('开始', '')

            if self.mysql_query(assets_name=assets_name[0], announcement_start_time=str_to_y_m_d_H_M_S(datetime_str)):
                continue

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id="{0}_{1}".format(self.website, origin_id),
                assets_name=assets_name[0],
                announcement_start_time=str_to_y_m_d_H_M_S(datetime_str),
                img_url="http:" + image_url[0],
                province=province[0],
                website=website,
                state=state[0],
                url=url
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        list = driver.find_elements(By.XPATH,
                                    '//*[@id="form1"]/div[10]/ul/li')

        n = 1
        data_list = []
        for i in list:
            data_dict = {}
            title = i.text
            content = driver.find_element(By.XPATH,
                                          f'//*[@id="ghnr{n}"]').get_attribute("outerHTML").replace(" ", "").replace(
                "\n", "")
            data_dict['title'] = title
            data_dict["content"] = content
            data_list.append(data_dict)

            n += 1

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=data_list)

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 2  # 写死20

        logtool.info("开始爬取网友拍")

        while maxpage >= minpage:
            url = f'http://www.wypai.net/bidlista0b1c0d{minpage}.html'
            a = self.data_list(url=url)

            # 解析列表页
            auction_infos = self.parse_data_list(html=a)

            for auction_info in auction_infos:
                driver = self.data_details(url=auction_info.url)
                time.sleep(3)

                # 解析详情页
                auction_info, auction_datail = self.parse_data_details(driver=driver, auction_info=auction_info)
                print(auction_info)

                id = self.insert_one_auction_info(auction_info.to_json())
                auction_datail.id = id
                self.insert_one_auction_detail(auction_datail.to_json())

            minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
