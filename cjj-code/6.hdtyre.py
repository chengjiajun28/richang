import os
# 文件目录
abs_path = os.path.abspath(__file__)
#print(abs_path[0:abs_path.find('auction')-1])
import sys
sys.path.append(abs_path[0:abs_path.find('auction')-1])

import time
from selenium.webdriver.common.by import By
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S
import re


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "hdtyre"

    # 列表
    def data_list(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    # 请求详情页
    def data_details(self, *args, **kwargs):
        url = kwargs.get("url")

        return self.get_selenium_obj(url=url)

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        time.sleep(3)

        global origin_id
        driver = kwargs.get("driver")

        list = driver.find_elements(By.XPATH, '//*[@id="c_portalResNews_list-15973702689761851"]/div/div/div[1]/div')
        auction_infos = []
        for i in list:
            # 网站原始id
            # origin_id: str
            a = i.find_element(By.XPATH, './/div[1]/div[2]/h3/a')
            url = a.get_attribute('href')
            origin_id = url.split("=")[1]

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + "_" + origin_id

            # 拍卖公告名称
            # assets_name: str
            assets_name = a.text

            # 报名开始时间
            # announcement_start_time: str

            # 报名截止时间
            # announcement_end_time: str
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
            # 城市
            # city: str
            # 县
            # county: str
            # 拍卖网站 标识符 可以是域名
            # website: str
            # 拍卖类型
            # assets_type: str
            name_type = ""
            if "车" in assets_name:
                name_type = self.jidongche
            else:
                name_type = self.wuzishebei

            # 关注数
            # onlookers: str
            # 状态
            # state: str
            # 拍卖链接
            # url: str
            url = url

            # sync_uat: bool = False
            # sync_prd: bool = False


            a = ['维修','修复','改造']
            if any(b in i for i in a):
                continue

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                # announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
                # img_url=img_url,
                # province=province,
                url=url,
                website=self.website,
                province="四川",
                assets_type=name_type
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(1)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        auction_info.announcement_start_time = str_to_y_m_d_H_M_S(driver.find_element(By.XPATH,
                                                                                      '//*[@id="ContentTxt"]/div/div/div[2]/div/div[2]/div/div[2]/table/tbody/tr[3]/td[1]').text)
        announcement_end_time = str_to_y_m_d_H_M_S(driver.find_element(By.XPATH,
                                                                       '//*[@id="ContentTxt"]/div/div/div[2]/div/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text)

        from datetime import datetime

        # 指定特定时间
        target_time_str = announcement_end_time
        target_time = datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")

        # 获取当前时间
        current_time = datetime.now()

        # 比较时间
        if target_time < current_time:
            return

        auction_info.announcement_end_time = announcement_end_time

        html = driver.find_element(By.XPATH,
                                   '//*[@id="content"]').get_attribute("outerHTML")

        details = [{
            "title": "详细信息",
            "content": html
        }]

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=html)

    def action(self, *args, **kwargs):
        a = 1
        minpage = 1
        maxpage = 20  # 写死20

        urls = ["http://www.hdtyre.com/news/15/#c_portalResNews_list-15973702689761851-",
                "http://www.hdtyre.com/news/18/#c_portalResNews_list-15973702689761851-",
                "http://www.hdtyre.com/news/21/#c_portalResNews_list-15973702689761851-"]

        logtool.info("开始爬取")
        logtool.info("获取列表")

        for url in urls:
            a = 1
            while minpage <= maxpage:
                url = url + str(minpage)
                driver = self.data_list(url=url)
                auction_infos = self.parse_data_list(driver=driver)
                for auction_info in auction_infos:
                    driver = self.data_details(url=auction_info.url)

                    time.sleep(2)
                    driver.refresh()
                    time.sleep(1)

                    if not self.parse_data_details(driver=driver, auction_info=auction_info):
                        a = 0
                        break

                    auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

                    if self.mysql_query(assets_name=auction_info.assets_name, announcement_end_time=auction_info.announcement_end_time):
                        continue


                    id = self.insert_one_auction_info(auction_info.to_json())
                    auction_detial.id = id
                    self.insert_one_auction_detail(auction_detial.to_json())
                    print(auction_info)

                if a == 0:
                    break

                minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
