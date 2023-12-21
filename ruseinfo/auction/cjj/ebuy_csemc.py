import time

import jionlp
import pandas as pd
import requests

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler
from ruseinfo.auction.cjj.file_utils import orc_request, process_expression, remove_path


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': 1,
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

        # 处理登录
        page = self.get_page_obj(url=url)

        user_name = "yanghao199081"
        pwd = "yanghao199081"

        page.ele('x://*[@id="uid"]').input(user_name)
        page.ele('x://*[@id="kl"]').input(pwd)

        # 处理图片验证码
        img = page('x://*[@id="img_rand_code"]')
        img.save('.\\img.png', '1.png')

        num = orc_request("img.png/1.png")
        a = process_expression(num)

        print(num, a)

        page.ele('x://*[@id="randCode"]').input(a)

        time.sleep(5)
        page.ele('x://*[@id="loginBt"]').click()

        remove_path('img.png/1.png')

        return page

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
        page = kwargs.get("page")

        datas = page.eles('x:/html/body/div[6]/div/div/div[2]/div[2]/div[1]/ul/li')

        return datas

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        page = kwargs.get("page")

        data = {}

        x详情页信息 = page.ele('x://div[@class="bd"]/div[3]').html
        详情页标题 = page.ele('x://div[@class="tit"]/label[1]').text
        保证金 = page.ele('x://div[@class="pricelist"]/ul[1]/li[1]/p[1]').text
        time_str = page.ele('x://div[@class="detail"]/p[2]/span[1]').text

        end_time = jionlp.parse_time(time_str)["time"][0]

        data["x详情页信息"] = x详情页信息
        data["详情页标题"] = 详情页标题
        data["保证金"] = 保证金
        data["结束时间"] = end_time
        data["页面网址"] = page.url

        page.back()

        return data

    def get_cokkie(self, *args, **kwargs):
        url = kwargs.get("url")

        page = self.get_page_obj(url=url)

        user_name = "yanghao199081"
        pwd = "yanghao199081"

        page.ele('x://*[@id="uid"]').input(user_name)
        page.ele('x://*[@id="kl"]').input(pwd)

        # 处理图片验证码
        img = page('x://*[@id="img_rand_code"]')
        img.save('.\\img.png', '1.png')

        num = orc_request("img.png/1.png")
        a = process_expression(num)

        page.ele('x://*[@id="randCode"]').input(a)
        page.ele('x://*[@id="loginBt"]').click()

        cookies = page.get_cookies()

        return cookies

    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 10  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        urls = [
            'http://wm.ebuy.csemc.com/wsplatform/index.do',
        ]

        # 请求列表页
        page = self.data_list(url=urls[0])

        time.sleep(3)

        page.ele('x:/html/body/div[6]/div/div/div[2]/div[3]/div[1]/ul/li[last()]').click()

        ruku_data = []
        # 翻页
        for i in range(maxpage):

            # 解析列表页
            datas = self.parse_data_list(page=page)

            n = 0

            # 循环列表
            for _, data in enumerate(datas):
                time.sleep(5)

                page.refresh()

                # 请求详情页
                page.eles('x:/html/body/div[6]/div/div/div[2]/div[2]/div[1]/ul/li')[_].click()

                time.sleep(5)

                # 解析详情页
                page_data = self.parse_data_details(page=page)

                ruku_data.append(page_data)

                n += 1

                print(f"第{i}页，第{n}条完成！！！")

            page.ele('x:/html/body/div[6]/div/div/div[2]/div[3]/div[2]/ul/li[last()]/a').click()
            page.wait.load_start()

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
