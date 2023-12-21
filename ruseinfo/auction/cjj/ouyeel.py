import random
import threading
import time

import pandas as pd

from ruseinfo.auction import logtool
from ruseinfo.auction.BaseCrawler import BaseCrawler


class Wk(BaseCrawler):
    ruku_data = []
    zz_ruku_data = []

    def __init__(self):
        super().__init__()

        self.website = "pmsearch_jd_jx"

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

        time.sleep(3)

        datas = page.eles('x:/html/body/div/div[2]/div[3]/section/section[2]/div[2]/div[1]/div')

        for mov1 in datas:
            image = mov1.ele('x:.//div[1]/img').link
            # '//*[@id="guid-2004318340"]/div/div/div[2]/a/div[1]/img'

            title_obj = mov1.ele('x:.//div[2]/div[1]/div[1]')

            title_obj_text = title_obj.text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")

            self.ruku_data.append(a)

    # 解析详情页
    def parse_data_details(self, i, ):

        # 请求详情页
        page = self.data_details(url=i["页面网址"], )

        time.sleep(5)

        for b in range(1, 9):
            time.sleep(1)
            page.scroll.to_location(300, 2500 * b)

        time.sleep(1)

        try:

            try:
                title_text = page.ele('x://*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[1]').text
            except Exception as e:
                title_text = page.ele('x://*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]').text

            保证金 = page.ele('x://*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[15]/ul/li[3]').text

            try:
                x详情页物介绍 = page.ele('x://div[@id="deposit-notes"]/div[2]').html
            except Exception as e:
                x详情页物介绍 = page.ele('x://div[@class="pm-ensureNotice"]').html

            x竞买公告 = page.ele('x://div[@id="bid-announce-content"]').html

            try:
                x竞买须知 = page.ele('x://div[@id="bid-notice-content"]').html
            except Exception as e:
                x竞买须知 = page.ele('x://ul[@class="floors"]/li[1]/div[1]/div[2]/p[2]').html

            try:
                x尾款支付说明 = page.ele('x://div[@id="addition-desc"]/div[2]/div[2]/div[1]').html
            except Exception as e:
                x尾款支付说明 = page.ele('x://ul[@class="floors"]/li[3]').html

            i["详情页标题"] = title_text
            i["保证金"] = 保证金
            i["x详情页物介绍"] = x详情页物介绍
            i["x竞买公告"] = x竞买公告
            i["x竞买须知"] = x竞买须知
            i["x尾款支付说明"] = x尾款支付说明

        except Exception as e:
            pass

        finally:
            page.quit()

            self.zz_ruku_data.append(i)

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
        maxpage = 2  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        url = "https://www.ouyeel.com/search-ng/exchange/search/bidding?biddingType=10"

        page = self.get_page_obj(url=url)

        time.sleep(2)

        n = 0

        # try:
        for i in range(5):

            datas = page.eles('x:/html/body/div/div[2]/div[3]/section/section[2]/div[2]/div[1]/div')

            for mov1 in datas:

                image = mov1.ele('x:.//div[1]/img').link
                # '//*[@id="guid-2004318340"]/div/div/div[2]/a/div[1]/img'

                title_obj = mov1.ele('x:.//div[2]/div[1]/div[1]')

                title_obj_text = title_obj.text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")

                title_obj.click()

                time.sleep(random.randint(1, 5))

                a = page.get_tab(page.latest_tab)

                time.sleep(1)

                # 停止页面加载
                # a.run_cdp('Page.stopLoading')

                for b in range(1, 5):
                    time.sleep(1)
                    a.scroll.to_location(300, 3000 * b)

                time.sleep(1)

                title_text = a.ele('x://*[@id="page-wrapper"]/div[1]/div[2]/div[1]/div[1]/h2').text
                保证金 = a.ele('x://*[@id="showDfyj"]').text
                地区 = a.ele('x://*[@id="tab-1"]/div[2]/div/table/tbody/tr[1]/td[2]').text
                x详情页物介绍 = a.ele('x://*[@id="tab-1"]/div[1]').html
                x联系信息 = a.ele('x://*[@id="tab-1"]/div[2]').html

                页面网址 = a.url

                tabs = page.tabs
                page.close_tabs(tabs[0])

                # 添加几行数据
                i = {
                    "详情页标题": title_text,
                    "保证金": 保证金,
                    "地区": 地区,
                    "x详情页物介绍": x详情页物介绍,
                    "x联系信息": x联系信息,
                    "页面网址": 页面网址,
                    '图片网址': image
                }

                self.zz_ruku_data.append(i)

                n += 1

            # 获取下一页按钮，有就点击
            btn = page.ele('x:/html/body/div/div[2]/div[3]/section/section[2]/div[2]/div[2]/div/div/button[2]')
            btn.click()
            page.wait.load_start()

        # 将字典列表转换为DataFrame对象
        df = pd.DataFrame(self.zz_ruku_data)

        # 使用to_csv()方法覆盖原有文件的内容
        df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')

        # # 请求列表页,
        # page = self.data_list(url=urls[0])
        #
        # time.sleep(random.randint(5, 10))
        #
        # # 解析列表页
        # self.parse_data_list(page_num=maxpage, page=page)
        #
        # datas = page.eles('x://*[@id="fm')
        #
        # # 循环列表
        # for _, i in enumerate(self.ruku_data):
        #     # 解析详情页
        #     t = threading.Thread(target=self.parse_data_details, args=(i,))
        #     t.start()
        #
        #     time.sleep(random.randint(5, 10))
        #
        #     print(f"第{_}条完成！！！")
        #
        # # 将字典列表转换为DataFrame对象
        # df = pd.DataFrame(self.zz_ruku_data)
        #
        # # 使用to_csv()方法覆盖原有文件的内容
        # df.to_csv(f"./csv/{self.website}.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    wk = Wk()
    wk.action()
