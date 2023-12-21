import time

import jionlp
import pandas as pd

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler
from ruseinfo.auction.cjj.file_utils import orc_request, process_expression, remove_path


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "norincogroup-ebuy_fj"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        # 处理登录
        page = self.get_page_obj(url=url)

        page('x://*[@id="gform"]/div/h4/span[2]').click()

        time.sleep(3)

        user_name = "yang199081"
        pwd = "Yanghao199081@"

        page.ele('x://*[@id="uid"]').input(user_name)
        page.ele('x://*[@id="kl"]').input(pwd)

        page('x://*[@id="img_rand_code"]').click()

        time.sleep(3)

        # 处理图片验证码
        img = page('x://*[@id="img_rand_code"]')
        img.save('.\\img.png', '2.png')

        num = orc_request("img.png/2.png")
        a = process_expression(num)

        print(num, a)

        page.ele('x://*[@id="randCode"]').input(a)

        time.sleep(5)
        page.ele('x://*[@id="loginBt"]').click()

        remove_path('img.png/2.png')

        return page

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")
        cookies = kwargs.get("cookies")

        page = self.get_page_obj(url=url, cookies=cookies)

        return page

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        page = kwargs.get("page")
        page_num = kwargs.get("page_num")

        url_datas = []

        # 处理详情页链接
        for i in range(page_num):

            datas = page.eles('x:/html/body/div[8]/div/div/div[2]/div[2]/div[1]/ul/li')
            #                   /html/body/div[8]/div/div/div[2]/div[2]/div[1]/ul/li[1]/dl/dd[2]/em

            for data in datas:
                id = data.attr("onclick")

                values = id.split('(')[1].split(')')[0].split(',')
                first_value = values[0]

                url = f"https://wm.norincogroup-ebuy.com/exp/auction/buy/bout/seeBout.do?boutid={first_value}"

                url = url.replace("'", "")

                url_datas.append(url)

            page.ele('x:/html/body/div[8]/div/div/div[2]/div[3]/div[2]/ul/li[last()]').click()

        # 获取cookie
        cookies = page.get_cookies()

        page.quit()

        return url_datas, cookies

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        page = kwargs.get("page")

        time.sleep(5)

        data = {}

        x详情页信息 = page.ele('x://*[@id="record"]/div[2]/div/div[3]').html
        详情页标题 = page.ele('x:/html/body/div[4]/div/div[2]/div[2]/div[2]/div[1]/label').text
        保证金 = page.ele('x:/html/body/div[4]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/ul/li[1]/p[1]').text
        time_str = page.ele('x:/html/body/div[4]/div/div[2]/div[2]/div[2]/div[2]/div[2]/p[2]/span').text

        end_time = jionlp.parse_time(time_str)["time"][0]

        data["x详情页信息"] = x详情页信息
        data["详情页标题"] = 详情页标题
        data["保证金"] = 保证金
        data["结束时间"] = end_time
        data["页面网址"] = page.url

        try:
            data["地区"] = page.ele('x://*[@id="record"]/div[2]/div/div[3]/div[2]/ul/li[last()]').text
        except Exception as e:
            data["地区"] = page.ele('x://*[@id="record"]/div[2]/div/div[3]/div[3]/ul/li[last()]').text

        return data

    def get_cookie(self, *args, **kwargs):
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
            'https://wm.norincogroup-ebuy.com/index.do',
        ]

        # 请求列表页
        page = self.data_list(url=urls[0])

        time.sleep(3)

        ruku_data = []

        # 解析列表页
        url_datas, cookies = self.parse_data_list(page_num=maxpage, page=page, )

        n = 0

        # 循环列表
        for _, url in enumerate(url_datas):
            time.sleep(5)

            # 请求详情页
            page = self.data_details(url=url, cookies=cookies)

            # 解析详情页
            page_data = self.parse_data_details(page=page)

            ruku_data.append(page_data)

            n += 1

            print(f"第{n}条完成！！！")

            page.quit()

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
