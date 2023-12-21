import os

import jionlp

# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys

from ruseinfo.auction import logtool
from ruseinfo.auction.Auction import Auction_Info, Auction_Detials
from ruseinfo.auction.BaseCrawler import BaseCrawler
from ruseinfo.tools import str_to_y_m_d_H_M_S

sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import requests

import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


def get_miyao():
    import requests

    cookies = {
        'SUNWAY-ESCM-COOKIE': '9770e778-fa1c-4fae-9fab-9f7c77814ba4',
        '__jsluid_s': '7b79ff19e788059184debcf08dac7874',
        'JSESSIONID': '89379D9DD0694958BA8AADCBCD9CC0E0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        # 'Cookie': 'SUNWAY-ESCM-COOKIE=9770e778-fa1c-4fae-9fab-9f7c77814ba4; __jsluid_s=7b79ff19e788059184debcf08dac7874; JSESSIONID=89379D9DD0694958BA8AADCBCD9CC0E0',
        'Origin': 'https://ec.minmetals.com.cn',
        'Referer': 'https://ec.minmetals.com.cn/logonAction.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.post('https://ec.minmetals.com.cn/open/homepage/public', cookies=cookies, headers=headers)

    return response.text


def encryption_assembly():
    # 执行 JavaScript 代码
    with open("./jss/ec_minmetals.js", "r", encoding="utf-8") as file:
        script_code = file.read()

    ctx = execjs.compile(script_code)
    return ctx


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': '__jsluid_s=573d9d87dfb361383444cbeb0fe353b3; SUNWAY-ESCM-COOKIE=a5327ce7-e475-4359-8920-8f41124c2a03; JSESSIONID=68F695D238DC010C8F8A51AD86A800C9',
            'Origin': 'https://ec.minmetals.com.cn',
            'Referer': 'https://ec.minmetals.com.cn/open/home/purchase-info?tabIndex=8',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.website = "ec_minmetals"

    # 列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")
        r = kwargs.get("r")

        # {
        #     "inviteMethod": "",
        #     "businessClassfication": "",
        #     "mc": "",
        #     "lx": "ZBGG",
        #     "dwmc": "",
        #     "pageIndex": 2
        # }

        h = {
            "inviteMethod": "",
            "mc": "",
            "lx": "ZBGG",
            "dwmc": "",
            "pageIndex": page
        }

        a = encryption_assembly()

        params = [h, r]

        result = a.call("haha", *params)

        json_data = {
            'param': result,
        }

        response = self.session.post(url=url, json=json_data)

        return response.json()["list"]

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")
        id = kwargs.get("id")
        r = kwargs.get("r")

        h = {
            "id": id,
        }

        a = encryption_assembly()

        params = [h, r]

        result = a.call("haha", *params)

        json_data = {
            'param': result,
        }

        response = self.session.post(url=url, json=json_data)

        return response.json()["obj"]

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        list_pages = kwargs.get("list_pages")

        auction_infos = []
        for i in list_pages:

            # 网站原始id
            # origin_id: str
            origin_id = i["bm"]

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + "_" + origin_id

            # 拍卖公告名称
            # assets_name: str
            assets_name = i["mc"]

            # 报名开始时间
            # announcement_start_time: str

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

            diqu = jionlp.parse_location(i["dwmc"])

            # 省份
            # province: str
            province = diqu.get("province")

            # 城市
            # city: str
            city = diqu.get("city")

            # 县
            # county: str

            # 拍卖网站 标识符 可以是域名
            # website: str
            website = self.website

            mysql_classification = self.select_mysql_classification()

            # 拍卖类型
            # assets_type: str
            assets_type = "其它"
            for haha in mysql_classification:
                # 判断需要的筛选词是否为空
                if not haha[0]:
                    continue

                # 判断需要的筛选词是否为空
                if not haha[1]:
                    continue

                # 移除列表中的空格
                words_list = [word for word in haha[1].split(',') if word != '']

                # 筛选不要的
                if haha[2]:
                    # 移除列表中的空格
                    words_list1 = [word1 for word1 in haha[2].split(',') if word1 != '']

                    if any(i in assets_name for i in words_list1):
                        continue

                if any(i in assets_name for i in words_list):
                    assets_type = haha[0]

                    break

            # 关注数
            # onlookers: str

            # 状态
            # state: str

            # 拍卖链接
            # url: str
            a = f"https://ec.minmetals.com.cn/open/home/purchase-info?id={origin_id}&lx=jpgg"
            url = a

            # sync_uat: bool = False
            # sync_prd: bool = False

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                url=url,
                # announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
                # img_url=img_url,
                # province=province,
                website=self.website,
                province=province,
                city=city,
                # state=state[0],
                assets_type=assets_type
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        deta_data = kwargs.get("deta_data")
        auction_info = kwargs.get("auction_info")

        # 拍卖链接
        # url: str

        # 网站原始id
        # origin_id: str

        # 拍卖标的ID
        # auction_id: str

        # 报名开始时间
        # announcement_start_time: str
        announcement_start_time = str_to_y_m_d_H_M_S(deta_data["wbinfo"]["textstarttime"])
        auction_info.announcement_start_time = announcement_start_time

        # 报名截止时间
        # announcement_end_time: str
        announcement_end_time = str_to_y_m_d_H_M_S(deta_data["wbinfo"]["textendtime"])
        auction_info.announcement_end_time = announcement_end_time

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

        # 城市
        # city: str

        # 县
        # county: str

        # 拍卖网站 标识符 可以是域名
        # website: str

        # 关注数
        # onlookers: str

        # 状态
        # state: str

        # content = ""
        # for data in deta_data["wzlist"]:
        #     content += "（" + data["goodsDesc"].replace(" ", "") + "）"
        #     content += "（" + data["goodsUnit"].replace(" ", "") + "）"
        #     content += "（" + str(int(data["goodsCount"])).replace(" ", "") + "）"
        #     content += "（" + str_to_y_m_d_H_M_S(data["shipmentDate"]).replace(" ", "") + "）" + "\n"

        details = deta_data["wbinfo"]['textcontent']

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=details)

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 20  # 写死20
        page_url = 'https://ec.minmetals.com.cn/open/homepage/zbs/by-lx-page'
        deta_url = "https://ec.minmetals.com.cn/open/homepage/zbs/zbgg"

        logtool.info("开始爬取")

        while minpage <= maxpage:
            logtool.info(f"获取{minpage}页列表")

            r = get_miyao()

            list_pages = self.data_list(url=page_url, page=minpage, r=r)

            auction_infos = self.parse_data_list(list_pages=list_pages)

            for auction_info in auction_infos:

                while True:
                    try:
                        r = get_miyao()
                        break
                    except Exception as e:
                        pass

                deta_data = self.data_details(url=deta_url, id=auction_info.origin_id, r=r)

                try:
                    auction_info, auction_detial = self.parse_data_details(deta_data=deta_data,
                                                                           auction_info=auction_info)
                except Exception as e:
                    continue

                logtool.info(f"{minpage}数据入库")
                id = self.insert_one_auction_info(auction_info.to_json())
                auction_detial.id = id
                self.insert_one_auction_detail(auction_detial.to_json())

                print(auction_info)
                print(auction_detial)

            minpage += 1


if __name__ == '__main__':
    # 获取分类数据

    wk = Wk()
    wk.action()
