import threading
import time

import pandas as pd

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler


class Wk(BaseCrawler):
    ruku_data = []

    def __init__(self):
        super().__init__()

        self.website = "zc_taobao"

    # 请求列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")
        cookies = kwargs.get("cookies")

        # 处理登录
        page = self.get_page_obj(url=url, cookies=cookies)

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

            time.sleep(3)

            datas = page.eles('x://*[@id="guid-2004318340"]/div/div/div')
            #                   //*[@id="guid-2004318340"]/div/div/div[1]/a

            for data in datas:
                url = data.ele('x:.//a').attr("href")

                url_datas.append(url)

            # 判断页面是否有新的数据
            if len(url_datas) % 48 != 0:
                break

            page.ele('x://*[@id="guid-2708524060"]/div/div[2]').click()

        page.quit()

        return url_datas

    # 解析详情页
    def parse_data_details(self, url, cookies):

        page = self.data_details(url=url, cookies=cookies)

        time.sleep(5)

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
            page.quit()

            self.ruku_data.append(data)

    def get_cookie(self, *args, **kwargs):
        url = kwargs.get("url")

        page = self.get_page_obj(url=url)

        user_name = "17168360408"
        pwd = "040828cjj"

        page.ele('x://*[@id="fm-login-id"]').input(user_name)
        page.ele('x://*[@id="fm-login-password"]').input(pwd)

        time.sleep(5)

        page.ele('x://*[@id="login-form"]/div[4]/button').click()

        time.sleep(20)

        cookies = page.get_cookies()

        page.quit()

        return cookies

    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 45  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        urls = [
            "https://login.taobao.com/member/login.jhtml?f=top&redirectURL=https%3A%2F%2Fzc-paimai.taobao.com%2Fwow%2Fpm%2Fdefault%2Fpc%2Fzichansearch%3Fpmid%3D0144569595_1685414424109%26pmtk%3D20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump%26path%3D27064540%2C27181431%26fcatV4Ids%3D%5B%2522206051702%2522%5D%26page%3D1%26spm%3Da2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1%26scm%3D20140647.julang.360_search.brand",
        ]

        list_urls = [
            # 工业用房
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[%22206051702%22]&statusOrders=[%221%22]',
            # 机动车
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[206137507,206146502,206149901]&statusOrders=[%221%22]',
            #     船舶
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[%22206067401%22]&statusOrders=[%221%22]',
            # #     其他交通工具
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[206137507,206146502,206149901]',
            # #     土地
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[%22206067101%22]&statusOrders=[%221%22]',
            # #     机械设备
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[%22206067101%22]&statusOrders=[%221%22]',
            # #     原材料边角料
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[%22206067101%22]&statusOrders=[%221%22]',
            # # 挖掘机
            'https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?pmid=0144569595_1685414424109&pmtk=20140647.0.0.0.27064540.puimod-pc-search-navbar_5143927030.vault-jump&path=27064540,27181431&page=1&spm=a2129.27181431.puimod-zc-focus-2021_2860107850.category-4-1&scm=20140647.julang.360_search.brand&fcatV4Ids=[%22206148603%22]&statusOrders=[%221%22]',
        ]

        # 处理登录
        cookies = self.get_cookie(url=urls[0])

        # 处理详情页链接
        datas_urls = []
        for url in list_urls:
            # 请求列表页,
            page = self.data_list(url=url, cookies=cookies)

            time.sleep(3)

            # 解析列表页
            url_datas = self.parse_data_list(page_num=maxpage, page=page, )

            for i in url_datas:
                datas_urls.append(i)

        # 详情页链接去重
        my_set = set(datas_urls)
        datas_urls = list(my_set)

        # 循环列表
        for _, url in enumerate(datas_urls):
            # 解析详情页
            t = threading.Thread(target=self.parse_data_details, args=(url, cookies,))
            t.start()

            time.sleep(3)

            print(f"第{_}条完成！！！")

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(self.ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
