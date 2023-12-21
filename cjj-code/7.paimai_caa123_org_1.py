import os
# 文件目录
abs_path = os.path.abspath(__file__)
#print(abs_path[0:abs_path.find('auction')-1])
import sys
sys.path.append(abs_path[0:abs_path.find('auction')-1])

import re

import logtool
import time
from selenium.webdriver.common.by import By
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S
import requests
import jionlp as jio


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "paimai_caa123_org"

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
        driver = kwargs.get("driver")
        id = kwargs.get("id")

        data_list = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div[2]/div/ul/li')

        auction_infos = []
        for i in data_list:
            # 网站原始id
            # origin_id: str
            url = i.find_element(By.XPATH, './/a').get_attribute('href')

            pattern = r"\?lotId=(\d+)"

            matches = re.findall(pattern, url)

            origin_id = matches[0]

            # 拍卖标的ID
            # auction_id: str
            auction_id = self.website + "_" + origin_id

            # 拍卖公告名称
            # assets_name: str
            assets_name = i.find_element(By.XPATH, './/a/p').text

            op = ["碳砖", "摩擦", "系统", "木板", "苯胺", "核磁", "木托", "味精", "湿渣", "催化", "保护", "液压油",
                  "机械油", "乙二醇", "机油", "轮油", "稀酰胺", "酸脂", "化铝", "活性炭", "分子筛", "硫酸", '药品',
                  "树脂", "废液", "瓷球", "化汞", "乙烯", "袋子", "号楼", "树枝", "房屋", 'PVC', "皮带", "过滤", "元件",
                  "石墨", "粉末", "电池", "首饰", "晶硅", "凳子", "椅子", "棉被", "环保", "编织", "土料", "树木",
                  "摩托", "股权", "砂石", "棱砖", "方砖", "压块", "河沙", "除灰", "石灰", "玻璃", "草坪", "塑胶",
                  "接头", "甲醇", "监测", "废甲", "布袋", "手机", "电脑", "收账", "服务", "义务", "附6号", "土壤",
                  "经营", "渣土", "粗苯", "焦油", "溶液", "茶砖", "茶饼", "酒", "林权", "南瓜"]

            if any(assets_name in i for i in op):
              print(1)

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = i.find_element(By.XPATH, './/a/div[2]/div/p[1]/span[2]/span').text
            # '//a/div[2]/div/p[1]/span[2]/span/text()'

            if "结束" in announcement_start_time:
                continue

            # 报名截止时间
            # announcement_end_time: str

            # 保证金
            # deposit: str

            # 图片url
            # img_url: str
            img_url = "https://paimai.caa123.org.cn" + i.find_element(By.XPATH, './/a/div[1]/img').get_attribute('src')

            # imgPaths前缀
            # img_prefix: str
            # img_prefix = 'https://paimai.ca   a123.org.cn/'

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
            try:
                onlookers = i.find_element(By.XPATH, './/a/div[3]/div/p/span[1]').text
            except Exception as e:
                onlookers = ""
                pass

            # 状态
            # state: str
            try:
                if "开始" not in i.find_element(By.XPATH, './/a/div[2]/div[1]/p[2]/input').get_attribute('value'):
                    continue
                state = i.find_element(By.XPATH, './/a/div[2]/div[1]/p[2]/input').get_attribute('value')
            except Exception as e:
                state = ""
                pass
            # 拍卖链接
            # url: str
            url = url

            # sync_uat: bool = False
            # sync_prd: bool = False




            if mysql_query(assets_name=assets_name, announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time)):
                continue




            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                # announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
                # province=province,
                announcement_start_time=announcement_start_time,
                url=url,
                website=self.website,
                assets_type=name_type,
                state=state,
                onlookers=onlookers,
                img_url=img_url,

            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        time.sleep(1)
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        # 时间
        shijian = driver.find_element(By.XPATH, '//*[@id="DISPLAY_BID_COMMING"]/ul/li[1]').text

        if '即将开始拍卖会正在进行中' in shijian or "拍卖会已开始" in shijian:
            return Auction_Detials()

        import re
        from datetime import datetime

        # 原始时间字符串
        original_time_str = shijian

        # 使用正则表达式提取日期和时间部分
        date_match = re.search(r'(\d{4}年\d{2}月\d{2}日)', original_time_str)
        time_match = re.search(r'(\d{2}:\d{2})开始', original_time_str)

        if date_match and time_match:
            date_str = date_match.group(1)
            time_str = time_match.group(1)

            # 重新格式化日期和时间
            formatted_time = f"{re.sub(r'年|月', '-', date_str)} {time_str}"
            # 将原始日期时间字符串解析为datetime对象
            original_date_time = datetime.strptime(formatted_time, "%Y-%m-%d日 %H:%M")

            # 将datetime对象格式化为目标日期时间字符串格式
            target_date_time_str = original_date_time.strftime("%Y-%m-%d %H:%M")
            auction_info.announcement_start_time = str_to_y_m_d_H_M_S(target_date_time_str)

        baozhengjing = driver.find_element(By.XPATH, '//*[@id="cashDeposit"]').text.replace(",", "")
        auction_info.deposit = baozhengjing

        b = jio.parse_location(driver.find_element(By.XPATH, '//*[@id="NoticeDetail"]').text)

        auction_info.province = b.get("province")
        if not auction_info.province:
            auction_info.province = "四川省"

        auction_info.city = b.get("city")

        # 图片
        image_urls = driver.find_elements(By.XPATH, '//*[@id="RemindTip"]/div[4]/div[2]/img')
        auction_info.img_paths = ""
        for image_url in image_urls:
            url = image_url.get_attribute('src')
            auction_info.img_paths += ";" + url
        auction_info.img_paths = auction_info.img_paths[1:]

        title = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/ul/li[1]').text
        if title == "重要提示":
            title = title
            content = driver.find_element(By.XPATH, '//*[@id="DetailTabMain"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")
            title1 = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/ul/li[2]').text
            content1 = driver.find_element(By.XPATH, '//*[@id="NoticeDetail"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")
            title2 = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/ul/li[3]').text
            content2 = driver.find_element(By.XPATH, '//*[@id="ItemNotice"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")
            # title3 = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/ul/li[4]').text
            # content3 = driver.find_element(By.XPATH, '//*[@id="DetailTabMain"]').get_attribute(
            #     "outerHTML").replace(" ", "").replace("\n", "")
            title3 = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/ul/li[5]').text
            content3 = driver.find_element(By.XPATH, '//*[@id="RecordContent"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")

            details = [
                {
                    "title": title,
                    "content": content,
                }, {
                    "title": title1,
                    "content": content1,
                }, {
                    "title": title3,
                    "content": content3,
                }, {
                    "title": title2,
                    "content": content2,
                },
            ]

        else:
            title = title
            content = driver.find_element(By.XPATH, '//*[@id="NoticeDetail"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")
            title1 = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/ul/li[2]').text
            content1 = driver.find_element(By.XPATH, '//*[@id="ItemNotice"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")
            # title2 = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/ul/li[3]').text
            # content2 = driver.find_element(By.XPATH, '//*[@id="DetailTabMain"]').get_attribute(
            #     "outerHTML").replace(" ", "").replace("\n", "")
            title3 = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/ul/li[4]').text
            content3 = driver.find_element(By.XPATH, '//*[@id="RecordContent"]').get_attribute(
                "outerHTML").replace(" ", "").replace("\n", "")

            details = [
                {
                    "title": title,
                    "content": content,
                }, {
                    "title": title1,
                    "content": content1,
                }, {
                    "title": title3,
                    "content": content3,
                },
            ]

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=details)

    def action(self, *args, **kwargs):

        urls = [
            "https://paimai.caa123.org.cn/pages/lots/list.html?&status=0&attribute=&term=&startTimeStamp=&endTimeStamp=&standardType=20&secondaryType=&canLoan=&isRestricted=&insuranceSupport=&num=",
            'https://paimai.caa123.org.cn/pages/lots/list.html?&status=0&attribute=&term=&startTimeStamp=&endTimeStamp=&standardType=255&secondaryType=&canLoan=&isRestricted=&insuranceSupport=&num=',
            'https://paimai.caa123.org.cn/pages/lots/list.html?&status=0&attribute=&term=&startTimeStamp=&endTimeStamp=&standardType=19&secondaryType=&canLoan=&isRestricted=&insuranceSupport=&num=',
            'https://re.caa123.org.cn/pages/exponebdlist.html?&status=0&term=&startTimeStamp=&endTimeStamp=&canLoan=&isRestricted=&num=',
            'https://paimai.caa123.org.cn/pages/financeassets/financelist.html?&status=0&term=&startTimeStamp=&endTimeStamp=&standardType=20&secondaryType=&canLoan=&isRestricted=&insuranceSupport=&num=',
            'https://paimai.caa123.org.cn/pages/bankruptcyassets/bankruptlist.html?&status=0&term=&startTimeStamp=&endTimeStamp=&standardType=20&secondaryType=&canLoan=&isRestricted=&insuranceSupport=&num=',
            'https://paimai.caa123.org.cn/pages/bankruptcyassets/bankruptlist.html?&status=0&term=&startTimeStamp=&endTimeStamp=&standardType=255&secondaryType=&canLoan=&isRestricted=&insuranceSupport=&num=',
            'https://paimai.caa123.org.cn/pages/bankruptcyassets/bankruptlist.html?&status=0&term=&startTimeStamp=&endTimeStamp=&standardType=19&canLoan=&isRestricted=&insuranceSupport=&num=',
        ]

        for url in urls:
            minpage = 0
            maxpage = 2  # 写死20X

            while minpage < maxpage:
                logtool.info(f"第{minpage}页")
                url1 = url + str(minpage)

                driver = self.data_list(url=url1)
                time.sleep(3)

                auction_infos = self.parse_data_list(driver=driver)

                if not auction_infos:
                    break

                # 处理详情页
                for auction_info in auction_infos:
                    time.sleep(2)
                    driver = self.data_details(url=auction_info.url)

                    try:
                        auction_info, auction_detial = self.parse_data_details(driver=driver, auction_info=auction_info)

                        id = self.insert_one_auction_info(auction_info.to_json())
                        auction_detial.id = id
                        self.insert_one_auction_detail(auction_detial.to_json())
                        print(auction_info)
                        print(auction_detial)

                    except Exception as e:
                        continue

                minpage += 1


if __name__ == '__main__':
    wk = Wk()
    wk.action()
