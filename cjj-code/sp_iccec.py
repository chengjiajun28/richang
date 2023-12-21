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
from urllib.parse import quote
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
        self.website = "sp_iccec"

        headers = {
            'APP_TOKEN': '',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': '',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            # 'Cookie': 'language=zh-cn; HWWAFSESID=c3fe0767d7af75e260; HWWAFSESTIME=1694412088532',
            'Origin': 'https://sp.iccec.cn',
            'Referer': 'https://sp.iccec.cn/searchList?type=98',
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

    # 请求列表页
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")

        json_data = {
            'pageNo': page,
            'pageSize': 10,
            'noticeTitle': '',
            'sortName': '1',
            'sortOrder': '0',
            'supCodeList': [],
            'purchaseCategory': '',
            'purchaseType': [],
            'purchaseClassList': [],
            'matBigClasses': [
                '01',
                '05',
                '06',
                '07',
                '99',
            ],
            'agentId': 100123,
            'languageType': 'zh-cn',
        }

        response = self.session.post(url=url, json=json_data)

        return response.json()["data"]["rows"]

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表页
    def parse_data_list(self, *args, **kwargs):
        res = kwargs.get("res")

        auction_infos = []
        for i in res:
            # 网站原始id
            # origin_id: str
            origin_id = i["schemeId"]

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + "_" + str(origin_id)

            # 拍卖公告名称
            # assets_name: str
            assets_name = i["noticeTitle"]

  
            a = ["废", "拆除", "钢"]
            if not any(assets_name in i for i in a):
                continue

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = str_to_y_m_d_H_M_S(i["noticeStartTime"])

            # 报名截止时间
            # announcement_end_time: str
            announcement_end_time = str_to_y_m_d_H_M_S(i["firstRoundEndTime"])

            if announcement_end_time:
                # 判断时间
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
            import jionlp as jio

            b = jio.parse_location(assets_name)
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
            state = "正在进行"

            # 拍卖链接
            # url: str
            url = f"https://sp.iccec.cn/viewNoticeDetail?schemeId={i['schemeId']}&schemeCode={quote(i['schemeCode'])}&schemeName={quote(i['schemeName'])}&noticeId={i['noticeId']}&opUnitName={quote(i['opUnitName'])}&opUnitId={i['opUnitId']}&purchaseType={i['purchaseType']}&schemeStatus={i['schemeStatus']}&checkFlag={i['checkFlag']}&supCode={i['supCode']}&supName={i['supName']}"


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
                assets_type=assets_type,
                state=state,
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
                                      '//*[@id="app"]/div/div[2]/div/section/div/div/div[3]/div/div[5]/div/div[3]/div[1]').get_attribute(
            "outerHTML").replace(" ", "").replace("\n", "").replace("\t", "")

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
            "https://sp.iccec.cn/apis/sp/bidc/users/signup/searchSupNoticeNew",
        ]

        logtool.info("开始")

        while minpage < maxpage:
            # 请求列表页
            res = self.data_list(url=urls[0], page=minpage)

            # 解析列表页
            auction_infos = self.parse_data_list(res=res)

            for auction_info in auction_infos:
                driver = self.data_details(url=auction_info.url)

                auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)
                id = self.insert_one_auction_info(auction_info.to_json())
                auction_detial.id = id
                self.insert_one_auction_detail(auction_detial.to_json())

                print(auction_info)
                print(auction_detial)

            minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
