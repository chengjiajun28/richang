import random
import time

import pandas as pd
import requests

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler
from ruseinfo.auction.cjj.file_utils import orc_request, remove_path


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.cookies = {
            'AlteonPcgmh': '0a03b7f633d5867f1f41',
            'wasteAreaValue': '8c4745ca-ad90-4086-823c-c506ab6e9fb9',
        }

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            # 'Cookie': 'AlteonPcgmh=0a03b7f633d5867f1f41; wasteAreaValue=cd0127a0-1e56-440b-a341-23cfa53499c9',
            'DNT': '1',
            'Referer': 'https://cg.95306.cn/bfwz/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.website = "cg_95306"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        page = kwargs.get("page")

        params = {
            'bidType': '10',
            'professionalCode': '00',
            'noticeType': '01',
            'createPeopUnit': '',
            'wzType': '',
            'inforCode': '',
            'startDate': '',
            'endDate': '',
            'pageNum': page,
            'pageSize': '10',
            'jointSaleType': '',
            'r': time.time(),
        }

        response = self.session.get(url=url, params=params, cookies=self.cookies)

        return response.json()["data"]["resultData"]["result"]

    # 请求详情页
    def data_details(self, *args, **kwargs):
        id = kwargs.get("id")

        url = 'https://cg.95306.cn/proxy/portal/elasticSearch/scrapSuppliesIndexView'

        params = {
            'noticeId': id,
            'r': time.time(),
        }

        response = self.session.get(url=url, params=params, cookies=self.cookies)
        return response.json()

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        json_data = kwargs.get("json_data")

        datas = []
        ids = []
        for i in json_data:
            title = i["notTitle"]
            start_time = i["checkTime"]
            # end_time = i["offerStartTime"]
            # area = i["detailAddress"]

            url = f"https://cg.95306.cn/bfwz/#/annDetails?id={i['id']}"

            data = {
                "详情页标题": title,
                "页面网址": url,
                # "地区": area,
                '开始时间': start_time,
                # '结束时间': end_time,

            }

            ids.append(i['id'])
            datas.append(data)

        return ids, datas

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        data_json = kwargs.get("data_json")
        data = kwargs.get("data")

        x详情页信息 = data_json["data"]["noticeContent"]["notCont"]

        data["x详情页信息"] = x详情页信息

        return data

    def get_token(self, *args, **kwargs):
        url = kwargs.get("url")

        page = self.get_page_obj(url=url)

        time.sleep(5)
        try:

            # 处理图片验证码
            img = page('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[2]/img')
            img.save('.\\img.png', '3.png')

            num = orc_request("img.png/3.png")

            page.ele('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[1]/div/div/div/input').input(num)

            time.sleep(5)
            page.ele('x://*[@id="app"]/div/div[4]/div/div[3]/span/button/span').click()

            remove_path('img.png/3.png')


        except Exception as e:
            pass

        cookies = page.get_cookies()[0]

        page.quit()
        return cookies

    def get_1_cookies(self):
        url = "https://cg.95306.cn/bfwz/#/announ?curIndex=2"

        page = self.get_page_obj(url=url)

        time.sleep(5)

        # 处理图片验证码
        img = page('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[2]/img')
        img.save('.\\img.png', '3.png')

        num = orc_request("img.png/3.png")

        page.ele('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[1]/div/div/div/input').input(num)

        time.sleep(5)
        page.ele('x://*[@id="app"]/div/div[4]/div/div[3]/span/button/span').click()

        remove_path('img.png/3.png')

        while True:
            try:

                page.ele('x:/html/body/div[2]/div/div[3]/button/span').click()

                time.sleep(5)
                page.ele('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[2]/img').click()

                # 处理图片验证码
                img = page('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[2]/img')
                img.save('.\\img.png', '3.png')

                num = orc_request("img.png/3.png")

                page.ele('x://*[@id="app"]/div/div[4]/div/div[2]/div/form/div/div[1]/div/div/div/input').input(num)

                time.sleep(5)
                page.ele('x://*[@id="app"]/div/div[4]/div/div[3]/span/button/span').click()

                remove_path('img.png/3.png')

            except Exception as e:
                break

        cookies = page.get_cookies()[0]

        page.quit()

        return cookies

    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 20  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        urls = [
            'https://cg.95306.cn/proxy/portal/elasticSearch/scrapSuppliesQueryDataToEs',
            'https://cg.95306.cn/proxy/portal/elasticSearch/scrapSuppliesIndexView',
        ]

        ruku_data = []
        # 翻页
        for i in range(maxpage):

            try:
                # 请求列表页
                json_data = self.data_list(url=urls[0], page=i + 1)
            except Exception as e:
                self.cookies = self.get_1_cookies()

                # 请求列表页
                json_data = self.data_list(url=urls[0], page=i + 1)

            # 解析列表页
            ids, datas = self.parse_data_list(json_data=json_data)

            n = 0

            # 循环列表
            for data, id in zip(datas, ids):

                while True:
                    try:
                        # 请求详情页
                        data_json = self.data_details(id=id, headers=self.headers)

                        time.sleep(random.randint(3, 10))

                        # 解析详情页
                        data = self.parse_data_details(data_json=data_json, data=data)

                        break
                    except Exception as e:

                        cookies = self.get_token(url=data["页面网址"])

                        self.cookies = cookies

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
