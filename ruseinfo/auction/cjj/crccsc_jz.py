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

        self.website = "crccsc_zb"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")

        params = {
            'page': page + 1,
            'type': '1',
            'rows': '10',
        }

        response = self.session.get(url=url, params=params)

        return response.json()['data']['list']

    # 请求详情页
    def data_details(self, *args, **kwargs):
        id = kwargs.get("id")

        url = 'https://www.crccsc.com/api/purchaser/bidinformation/getInformationByuuids'

        params = {
            'uuids': id,
        }
        response = self.session.get(url=url, params=params)
        return response.json()

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        json_data = kwargs.get("json_data")

        datas = []
        ids = []
        for i in json_data:
            title = i["title"]
            start_time = i["bidNum"]
            # end_time = i["offerStartTime"]
            # area = i["detailAddress"]

            url = f"https://www.crccsc.com/static/crccmall/#/webNewsNotice/{i['uuids']}"

            data = {
                "详情页标题": title,
                "页面网址": url,
                # "地区": area,
                '开始时间': start_time,
                # '结束时间': end_time,

            }

            ids.append(i['uuids'])
            datas.append(data)

        return ids, datas

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        data_json = kwargs.get("data_json")
        data = kwargs.get("data")

        x详情页信息 = data_json["data"]["content"]

        data["x详情页信息"] = x详情页信息

        return data

    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 5  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        urls = [
            'https://www.crccsc.com/api/purchaser/bidinformation/queryAllBinformationListForPage',
        ]

        ruku_data = []
        # 翻页
        for i in range(maxpage):

            # 请求列表页
            json_data = self.data_list(url=urls[0], page=i)

            # 解析列表页
            ids, datas = self.parse_data_list(json_data=json_data)

            n = 0

            # 循环列表
            for data, id in zip(datas, ids):
                # 请求详情页
                data_json = self.data_details(id=id, headers=self.headers)

                time.sleep(3)

                # 解析详情页
                data = self.parse_data_details(data_json=data_json, data=data)

                ruku_data.append(data)

                n += 1

                print(f"第{i}页，第{n}条完成！！！")

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
