import json
import time

import pandas as pd
import requests

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler


def get_token():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIwMjI3OTQsInVzZXJfbmFtZSI6IjE3MTMyNiIsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUiJdLCJqdGkiOiI1ZmYyYWZmOC04MzQxLTQ1OTMtYjM0ZS0yYTA5MmM3OGQyMDAiLCJjbGllbnRfaWQiOiJzdW50cmF5Iiwic2NvcGUiOlsiYWxsIl19.DbAp2DTa_1vRZOylH1OmNOuEtsimt8-Bh8AXjUtkIAc',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': 'HWWAFSESID=acc2876f2b4ff6da5e; HWWAFSESTIME=1702005163576; JSESSIONID=E02F659E5C12CBCE0F4722CECD2BF80C; isLogin=true; loginInfo=%7B%22userAccount%22%3A%2215308307366%22%2C%22password%22%3A%22eWFuZ2hhbzE5OTA4MQ%3D%3D%22%2C%22isAutoLogin%22%3Atrue%7D; subPlatform=; Authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIwMjI3OTQsInVzZXJfbmFtZSI6IjE3MTMyNiIsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUiJdLCJqdGkiOiI1ZmYyYWZmOC04MzQxLTQ1OTMtYjM0ZS0yYTA5MmM3OGQyMDAiLCJjbGllbnRfaWQiOiJzdW50cmF5Iiwic2NvcGUiOlsiYWxsIl19.DbAp2DTa_1vRZOylH1OmNOuEtsimt8-Bh8AXjUtkIAc; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIwMjI3OTQsInVzZXJfbmFtZSI6IjE3MTMyNiIsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUiJdLCJqdGkiOiI1ZmYyYWZmOC04MzQxLTQ1OTMtYjM0ZS0yYTA5MmM3OGQyMDAiLCJjbGllbnRfaWQiOiJzdW50cmF5Iiwic2NvcGUiOlsiYWxsIl19.DbAp2DTa_1vRZOylH1OmNOuEtsimt8-Bh8AXjUtkIAc; phone=; regType=1',
        'DNT': '1',
        'If-Modified-Since': '0',
        'Origin': 'https://www.crccsc.com',
        'Referer': 'https://www.crccsc.com/static/crccmall/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'userAccount': '15308307366',
        'password': 'eWFuZ2hhbzE5OTA4MQ==',
        'isAutoLogin': True,
        'loginIpStr': '{"cip":"127.0.0.1","cid":"00","cname":"未知"}',
    }

    response = requests.post('https://www.crccsc.com/api/sso/loginControl/login',
                             headers=headers,
                             json=json_data)

    return json.loads(response.json()["data"])["access_token"]


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': get_token(),
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'DNT': '1',
            'If-Modified-Since': '0',
            'Origin': 'https://www.crccsc.com',
            'Referer': 'https://www.crccsc.com/static/crccmall/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.website = "crccsc_xh"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")

        params = {
            'page': page + 1,
            'pageSize': '10',
            'orderKey': 'releaseTime',
            'order': 'desc',
        }

        response = self.session.get(url=url, params=params)

        return response.json()['data']['list']

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

        datas = []
        for i in json_data:
            title = i["title"]
            start_time = i["releaseTime"]
            end_time = i["offerStartTime"]
            area = i["detailAddress"]

            url = f"https://www.crccsc.com/static/crccmall/#/reuse/join/{i['uuids']}?type=detail"

            data = {
                "详情页标题": title,
                "页面网址": url,
                "地区": area,
                '开始时间': start_time,
                '结束时间': end_time,

            }

            datas.append(data)

        return datas

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        page = kwargs.get("page")
        data = kwargs.get("data")

        x竞价基本信息 = page.ele('x://div[@class="index__reuse--wMvpg"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]').html
        x竞价要求 = page.ele('x://div[@class="index__reuse--wMvpg"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]').html
        x标的物清单 = page.ele('x://div[@class="index__reuse--wMvpg"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[4]').html
        x竞价规则及费用要求 = page.ele(
            'x://div[@class="index__reuse--wMvpg"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[7]').html

        data["x竞价基本信息"] = x竞价基本信息
        data["x竞价要求"] = x竞价要求
        data["x标的物清单"] = x标的物清单
        data["x竞价规则及费用要求"] = x竞价规则及费用要求

        page.quit()

        return data

    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 5  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        urls = [
            'https://www.crccsc.com/api/reuse/index/moreScene',
        ]

        ruku_data = []
        # 翻页
        for i in range(maxpage):

            # 请求列表页
            json_data = self.data_list(url=urls[0], page=i)

            # 解析列表页
            datas = self.parse_data_list(json_data=json_data)

            # 循环列表
            for i in datas:
                # 请求详情页
                page = self.get_page_obj(url=i["页面网址"], headers=self.headers)

                time.sleep(10)

                # 解析详情页
                data = self.parse_data_details(page=page, data=i)

                ruku_data.append(data)

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
