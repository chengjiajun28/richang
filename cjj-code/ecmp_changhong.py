import os
# 文件目录
abs_path = os.path.abspath(__file__)
#print(abs_path[0:abs_path.find('auction')-1])
import sys
sys.path.append(abs_path[0:abs_path.find('auction')-1])

import re
import time

import requests
from selenium.webdriver.common.by import By
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
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'DNT': '1',
            'Origin': 'https://ecmp.changhong.com',
            'Referer': 'https://ecmp.changhong.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
            'neverCancel': 'true',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.session = requests.Session()
        self.session.headers.update(headers)
        self.website = "ecmp_changhong"

    # 列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")
        json_data = {
            'quickSearchValue': '',
            'quickSearchProperties': [
                'code',
                'name',
            ],
            'pageInfo': {
                'page': page,
                'rows': 30,
            },
            'sortOrders': [],
            'filters': [
                {
                    'fieldName': 'type',
                    'value': 'bid',
                    'operator': 'EQ',
                    'fieldType': 'string',
                },
            ],
        }
        response = self.session.post(url=url, json=json_data)
        return response.json()["rows"]

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        json_datas = kwargs.get("json_datas")

        auction_infos = []
        for json_data in json_datas:
            # 网站原始id
            origin_id = json_data["id"]

            # 拍卖标的ID
            auction_id = self.website + origin_id

            # 拍卖公告名称
            assets_name = json_data["title"]

            # 报名开始时间
            announcement_start_time = json_data["releaseTime"]
            # 报名截止时间
            announcement_end_time = json_data["participationTime"]

            # # 保证金
            # deposit: str
            # # 图片url
            # img_url: str
            # # imgPaths前缀
            # img_prefix: str
            # # 图片路径，多个分隔
            # img_paths: str
            # # 省份
            # province: str
            # # 城市
            # city: str
            # # 县
            # county: str

            # 拍卖网站 标识符 可以是域名
            website = self.website

            # 拍卖类型
            assets_type = ""
            if "车" in assets_name:
                assets_type = self.jidongche
            else:
                assets_type = self.wuzishebei

            # # 关注数
            # onlookers: str
            # # 状态
            state = json_data["statusEnumRemark"]
            # 拍卖链接
            # url = i.find_element(By.XPATH, './/a[1]').get_attribute('href')
            # sync_uat: bool = False
            # sync_prd: bool = False

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
                announcement_end_time=str_to_y_m_d_H_M_S(announcement_end_time),
                website=website,
                # img_url=img_url,
                # province=province,
                # state=state[0],
                assets_type=assets_type,
                province="四川",
                state=state,
                # url=url
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        json_data = kwargs.get("json_data")
        auction_info = kwargs.get("auction_info")

        detials = json_data["infText"]

        if not detials:
            url_id = json_data["previewId"]

            detials = [{
                "title": json_data["title"],
                "content": [{"title": json_data["title"],
                             "url": "https://ecmp.changhong.com/api-gateway/edm-service/preview/readFile?docId=" + url_id}]
            }]

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=detials)

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 1  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        url = 'https://ecmp.changhong.com/srm-pb-web/biddingInformation/listByPageNoAuth'

        while minpage <= maxpage:
            if maxpage == minpage and minpage != 1:
                break

            json_datas = self.data_list(url=url, page=minpage)

            auction_infos = self.parse_data_list(json_datas=json_datas)

            for json_data, auction_info in zip(json_datas, auction_infos):
                auction_info, auction_datails = self.parse_data_details(json_data=json_data, auction_info=auction_info)
                id = self.insert_one_auction_info(auction_info.to_json())
                auction_datails.id = id
                self.insert_one_auction_detail(auction_datails.to_json())
                print(auction_datails)

            minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
