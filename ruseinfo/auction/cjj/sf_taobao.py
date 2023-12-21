import threading
import time

import pandas as pd

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler


class Wk(BaseCrawler):
    ruku_data = []

    def __init__(self):
        super().__init__()

        self.website = "sf_taobao"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        page = self.get_page_user_obj(url=url, )

        return page

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        page = self.get_page_obj(url=url, )

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

            time.sleep(3)

            datas = page.eles('x:/html/body/div[3]/div[3]/div[3]/ul/li')
            #                   //*[@id="guid-2004318340"]/div/div/div[1]/a

            for data in datas:
                url = data.ele('x:.//a').attr("href")

                url_datas.append(url)

            # 判断页面是否有新的数据
            if len(url_datas) % 48 != 0:
                break

            page.ele('x:/html/body/div[3]/div[4]/a[last()]').click()

        return page,url_datas

    # 解析详情页
    def parse_data_details(self, page, url):

        page = page.new_tab(url=url)

        time.sleep(5)

        data = {}

        for b in range(1, 9):
            time.sleep(1)
            page.scroll.to_location(300, 2500 * b)

        time.sleep(1)

        try:
            title_text = page.ele('x://*[@id="page"]/div[4]/div/div/h1').text
            保证金 = page.ele('x://*[@id="J_HoverShow"]/tr[1]/td/span[2]/span').text
            地区 = page.ele('x://*[@id="itemAddress"]').text
            x详情页物介绍 = page.ele('x://*[@id="J_desc"]').html
            x竞买公告 = page.ele('x://*[@id="J_NoticeDetail"]').html
            x竞买须知 = page.ele('x://*[@id="J_ItemNotice"]').html
            x尾款支付说明 = page.ele('x://*[@id="J_CasePayInfo"]/div[2]').html

            data["详情页标题"] = title_text
            data["保证金"] = 保证金
            data["结束时间"] = page.ele('x://*[@id="sf-countdown"]/span[3]').text
            data["页面网址"] = page.url
            data["地区"] = 地区
            data["x详情页物介绍"] = x详情页物介绍
            data["x竞买公告"] = x竞买公告
            data["x竞买须知"] = x竞买须知
            data["x尾款支付说明"] = x尾款支付说明

        except Exception as e:
            pass

        finally:
            page.close()

            self.cache_mysql_datas(self.website, data)

            self.ruku_data.append(data)

    def action(self, *args, **kwargs):
        global page

        minpage = 0
        maxpage = 100  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        list_urls = [
            'https://sf.taobao.com/list/0__1.htm?spm=a213w.7398504.filter.1.2bc04fa7ZKgR9u&auction_source=0&st_param=-1&auction_start_seg=-1'
        ]

        # 处理详情页链接
        datas_urls = []
        for url in list_urls:
            # 请求列表页,
            page = self.data_list(url=url)

            time.sleep(3)

            # 解析列表页
            page, url_datas = self.parse_data_list(page_num=maxpage, page=page, )

            for i in url_datas:
                datas_urls.append(i)

        print(datas_urls)

        # 详情页链接去重
        my_set = set(datas_urls)
        datas_urls = list(my_set)

        # 循环列表
        for _, url in enumerate(datas_urls):
            # 解析详情页
            t = threading.Thread(target=self.parse_data_details, args=(page, url))
            t.start()

            time.sleep(5)

            print(f"第{_}条完成！！！")

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(self.ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
