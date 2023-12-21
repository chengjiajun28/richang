import os

# 文件目录
abs_path = os.path.abspath(__file__)
# # print(abs_path[0:abs_path.find('auction')-1])
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])

import re
import time
from datetime import datetime
from urllib.parse import unquote
from selenium.webdriver.common.by import By
import jionlp
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "sxcqsc_sxcqjy"

    # 请求列表页
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表页
    def parse_data_list(self, *args, **kwargs):
        time.sleep(3)
        driver = kwargs.get("driver")

        list = driver.find_elements(By.XPATH, '//*[@id="container"]/ul/li')

        auction_infos = []
        for i in list:
            # 网站原始id
            # origin_id: str
            url = i.find_element(By.XPATH, './/div[3]/div[1]/p[1]/a').get_attribute('href')

            match = re.search(r"detail/(.*?).html", url)
            if match:
                match = match.group(1)

            origin_id = match

            # 拍卖标的ID
            # auction_id: str
            auction_id = f"{self.website}_{origin_id}"

            # 拍卖公告名称
            # assets_name: str
            assets_name = i.find_element(By.XPATH, './/div[3]/div[1]/p[1]/a').text

            # 报名开始时间
            # announcement_start_time: str

            # 报名截止时间
            # announcement_end_time: str

            # 保证金
            # deposit: str

            # 图片url
            # img_url: str
            img_url = i.find_element(By.XPATH, './/div[1]/a/img').get_attribute('src')

            # imgPaths前缀
            # img_prefix: str

            # 图片路径，多个分隔
            # img_paths: str

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
            onlookers = i.find_element(By.XPATH, './/div[2]/p[2]/span[1]').text

            # 状态
            # state: str
            state = i.find_element(By.XPATH, './/div[2]/p[1]').text

            # 拍卖链接
            # url: str
            url = url

            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                # announcement_start_time=announcement_start_time,
                # announcement_end_time=announcement_end_time,
                onlookers=onlookers,
                img_url=img_url,
                # province=province,
                website=self.website,
                state=state,
                url=url,
                assets_type=assets_type,
                # city=city
            )

            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(2)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        a = driver.find_element(By.XPATH,
                                '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/ul/li[2]/p[2]').text

        # 省份
        # province: str
        import jionlp as jio

        b = jio.parse_location(a)
        auction_info.province = b.get("province")
        if not auction_info.province:
            auction_info.province = "四川省"

        # 城市
        # city: str
        auction_info.city = b.get("city")

        stra_time = driver.find_element(By.XPATH,
                                        '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[1]').text

        end_time = driver.find_element(By.XPATH,
                                       '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]').text

        auction_info.announcement_start_time = str_to_y_m_d_H_M_S(stra_time)
        auction_info.announcement_end_time = str_to_y_m_d_H_M_S(end_time)

        # 判断时间
        specified_time = datetime.strptime(auction_info.announcement_end_time, "%Y-%m-%d %H:%M:%S")
        # 获取当前时间
        current_time = datetime.now()
        # 判断当前时间是否大于指定时间
        if current_time > specified_time:
            return 0, 1

        details = [
            {
                "title": driver.find_element(By.XPATH,
                                             '/html/body/div[3]/div[3]/div/ul[1]/li[1]').text,
                "content": driver.find_element(By.XPATH,
                                               '/html/body/div[3]/div[3]/div/ul[2]/li[1]').get_attribute(
                    "outerHTML").replace(" ", "").replace("\n", "").replace("\t", "")

            },
            {
                "title": driver.find_element(By.XPATH,
                                             '/html/body/div[3]/div[3]/div/ul[1]/li[3]').text,
                "content": driver.find_element(By.XPATH,
                                               '/html/body/div[3]/div[3]/div/ul[2]/li[3]').get_attribute(
                    "outerHTML").replace(" ", "").replace("\n", "").replace("\t", "")

            },
            {
                "title": driver.find_element(By.XPATH,
                                             '/html/body/div[3]/div[3]/div/ul[1]/li[4]').text,
                "content": driver.find_element(By.XPATH,
                                               '/html/body/div[3]/div[3]/div/ul[2]/li[4]').get_attribute(
                    "outerHTML").replace(" ", "").replace("\n", "").replace("\t", "")

            }
        ]

        return auction_info, Auction_Detials(
            state=auction_info.state,
            url=auction_info.url,
            detials=details
        )

    # 启动函数
    def action(self, *args, **kwargs):
        minpage = 0
        maxpage = 1  # 写死20

        urls = [
            "https://sxcqsc.sxcqjy.cn/jyzx/list/FC",
        ]

        logtool.info("开始")

        # 请求列表页
        driver = self.data_list(url=urls[0])

        for g in range(maxpage):
            logtool.info(f"{minpage}")
            if g == 0:
                driver.find_element(By.XPATH, '//*[@id="subclass"]/a[4]').click()
            else:
                driver.find_element(By.XPATH, '//*[@id="subclass"]/a[5]').click()

            # 解析列表页
            auction_infos = self.parse_data_list(driver=driver)

            for auction_info in auction_infos:
                driver = self.data_details(url=auction_info.url)

                auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

                if auction_info == 0:
                    continue

                id = self.insert_one_auction_info(auction_info.to_json())
                auction_detial.id = id
                self.insert_one_auction_detail(auction_detial.to_json())

                print(auction_info)
                print(auction_detial)

            minpage += 1
            driver = self.data_list(url=urls[0])
            if g == 0:
                driver.find_element(By.XPATH, '//*[@id="subclass"]/a[4]').click()
            else:
                driver.find_element(By.XPATH, '//*[@id="subclass"]/a[5]').click()

            if len(auction_infos) == 8:
                for i in range(minpage):
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//*[@id="pagebar"]/a[6]').click()


if __name__ == '__main__':
    wk = Wk()
    wk.action()
