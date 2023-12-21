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
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            # 'Cookie': 'language=zh_CN; tenantId=3; companyId=1; groupId=3',
            'DNT': '1',
            'Referer': 'https://srm.chinaconch.com/oauth/public/default/public_info.html?bidType=WORNOUT',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

        self.website = "srm_chinaconch"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")
        id = kwargs.get("id")

        params = {
            'lang': 'zh_CN',
            'bidType': id,
            'page': page,
            'size': '10',
        }

        response = self.session.get(url=url, params=params)
        print(url)
        return response.json()["content"]

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")
        params = {
            'bidNoticeFlag': '0',
        }
        response = self.session.get(url=url, params=params)
        return response.json()

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        json_data = kwargs.get("json_data")

        auction_infos = []
        for data in json_data:
            # 网站原始id
            # origin_id: str
            origin_id = data["sourceHeaderId"]

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + str(origin_id)

            # 拍卖公告名称
            # assets_name: str
            assets_name = data["bidTitle"]

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = data["approvedDate"]

            # 报名截止时间
            # announcement_end_time: str
            announcement_end_time = data["quotationEndDate"]

            # 保证金
            # deposit: str

            # 图片url
            # img_url:

            # imgPaths前缀
            # img_prefix:

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
            website = self.website

            # 拍卖类型
            # assets_type: str
            if "车" in data["bidTypeMeaning"]:
                assets_type = self.jidongche
            else:
                assets_type = self.wuzishebei

            # 关注数
            # onlookers: str

            # 状态
            # state: str
            state = data["sourceCategoryMeaning"]

            # 拍卖链接
            # url: str
            url = f"https://srm.chinaconch.com/oauth/public/default/getBiddingDetail.html?sourceNum=null&sourceFrom=RFX&sourceType=BR&sourceHeaderId={origin_id}&showTable=false"

            sync_uat: bool = False
            sync_prd: bool = False

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
                state=state,
                province = "四川",
                assets_type=assets_type,
                url=url
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        data = kwargs.get("data")
        auction_info = kwargs.get("auction_info")

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=data["noticeContent"])

    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 20  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        url1 = 'https://srm.chinaconch.com/ssrc/v1/3/hlsn/oauth-source-notices/br-list/public'
        ids = ["EQUIPMENT", "WORNOUT"]

        while minpage <= maxpage:
            json_data = self.data_list(url=url1, page=minpage, id=ids[1])

            # 解析列表页
            auction_infos = self.parse_data_list(json_data=json_data)

            for auction_info in auction_infos:
                url = f"https://srm.chinaconch.com/ssrc/v1/3/hlsn/oauth-source-notices/RFX/BR/{auction_info.origin_id}/preview-site"
                print(auction_info, url)

                try:
                    data = self.data_details(url=url)
                except Exception as e:
                    continue
                auction_info, auction_datail = self.parse_data_details(data=data, auction_info=auction_info)

                # 入库
                id = self.insert_one_auction_info(auction_info.to_json())
                auction_datail.id = id
                self.insert_one_auction_detail(auction_datail.to_json())

            # 页数
            if len(json_data) < 10:
                minpage = maxpage + 1
            minpage += 1




if __name__ == '__main__':
    wk = Wk()
    wk.action()
