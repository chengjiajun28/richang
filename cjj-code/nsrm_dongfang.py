import os

# 文件目录
abs_path = os.path.abspath(__file__)
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
from datetime import datetime
from urllib.parse import unquote
import jionlp
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
            'Authorization': 'Bearer 1',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': 'caf_web_session=NDk4N2NhYTctODFjZS00MzAyLWE0ZTktZDM1YzNjM2Q1NTA0',
            'DNT': '1',
            'Origin': 'https://nsrm.dongfang.com',
            'Referer': 'https://nsrm.dongfang.com/platform/runtime/epp/designer/index.html?v=1694875027508',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
            'X-ECC-Current-Tenant': '1',
            'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

        self.website = "nsrm_dongfang_gkzbgg"

    # 请求列表页
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        type = kwargs.get("type")
        id = kwargs.get("id")
        page = kwargs.get("page")

        json_data = ""
        if id == 'GG,YG':
            json_data = {
                'pagesize': page,
                'pagenum': 10,
                'noticetitle': type,
                'rfqtype': 'CRFQ',
                'ggtype': id,
                'NOTICE_TYPE': 'NULL',
                'isopen': 1,
                'bntypecode': '06',
            }
        elif id == "G":
            json_data = {
                'pagesize': page,
                'pagenum': 10,
                'noticetitle': type,
                'rfqtype': 'CRFQ',
                'ggtype': 'G',
                'NOTICE_TYPE': 'NULL',
                'bntypecode': '09',
            }
        elif id == "GG":
            json_data = {
                'pagesize': page,
                'pagenum': 10,
                'noticetitle': type,
                'rfqtype': 'SRFQ',
                'ggtype': 'GG',
            }

        response = self.session.post(url=url, json=json_data)

        return response.json()

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表页
    def parse_data_list(self, *args, **kwargs):
        time.sleep(3)
        json_data = kwargs.get("json_data")

        auction_infos = []
        for i in json_data:
            # 网站原始id
            # origin_id: str
            origin_id = i['ID']

            # 拍卖标的ID
            # auction_id: str
            auction_id = f"{self.website}_{origin_id}"

            # 拍卖公告名称
            # assets_name: str
            assets_name = i['NOTICETITLE']

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = str_to_y_m_d_H_M_S(i["CREATETON"])

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

            b = jionlp.parse_location(assets_name)
            province = b.get("province")
            if not province:
                province = "四川省"

            # 城市
            # city: str
            city = b.get("city")

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
            # state: str

            # 拍卖链接
            # url: str
            url = f"https://nsrm.dongfang.com/platform/runtime/epp/designer/index.html?v=1694875027508#/eprocurementportal/detail?columnId=PublicBidding&type=zbxx&contentId={origin_id}"

            if self.mysql_query(assets_name=auction_title, announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time)):
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
                assets_type=assets_type,
                url=url,
                city=city,
            )

            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(3)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        details = driver.find_element(By.XPATH,
                                      '//*[@id="w392dd649-673d-4aed-a150-53d497d55f76"]/div/div/eprocurement-detail/div[1]/div/div').get_attribute(
            "outerHTML")
        # .replace(" ", "").replace("\n", "").replace("\t", "")

        return auction_info, Auction_Detials(
            state=auction_info.state,
            url=auction_info.url,
            detials=details
        )

    # 启动函数
    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 20  # 写死20

        urls = [
            'https://nsrm.dongfang.com/supplier/findEscrfqbillnoticesEntites',
        ]

        types = {
            "GG": ["废", "拆除", "钢"],
            "GG,YG": ["废", "拆除", "钢"],
            "G": ["废", "拆除", "钢"],
        }
        # 询价,竞价,公开

        for id in types:
            for type in types[id]:
                for page in range(1, maxpage):
                    logtool.info(f"{id}, {type},{page}")
                    # 请求列表页
                    res = self.data_list(url=urls[0], type=type, id=id, page=page)

                    # 解析列表页
                    auction_infos = self.parse_data_list(json_data=res["result"]["data"])

                    for auction_info in auction_infos:
                        driver = self.data_details(url=auction_info.url)

                        auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

                        id1 = self.insert_one_auction_info(auction_info.to_json())
                        auction_detial.id = id1
                        self.insert_one_auction_detail(auction_detial.to_json())

                        print(auction_info)
                        print(auction_detial)

                    if len(auction_infos) < 10:
                        break

        self.quit_driver()


if __name__ == '__main__':
    wk = Wk()
    wk.action()
