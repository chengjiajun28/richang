import os

# 文件目录
abs_path = os.path.abspath(__file__)
# print(abs_path[0:abs_path.find('auction')-1])
import sys

sys.path.append(abs_path[0:abs_path.find('auction') - 1])
import re
import time
from selenium.webdriver.common.by import By
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.website = "longdaoyun"

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
        driver = kwargs.get("driver")

        list = driver.find_elements(By.XPATH, '//*[@id="f1"]/div/div[1]/ul/li')

        auction_infos = []
        for i in list:
            if i.get_attribute('class') == "list-title bold clearfix":
                continue

            # 网站原始id
            origin_id = ""
            text = i.find_element(By.XPATH, './/a[1]').get_attribute('href')
            match = re.search(r"details/(.+?).html", text)
            if match:
                origin_id = match.group(1)

            # 拍卖标的ID
            auction_id = self.website + origin_id

            # 拍卖公告名称
            assets_name = i.find_element(By.XPATH, './/a[1]/p[1]').text

            # 报名开始时间
            announcement_start_time = i.find_element(By.XPATH, './/p[3]').text
            # 报名截止时间
            announcement_end_time = i.find_element(By.XPATH, './/p[2]').text

            # # 保证金
            # deposit: str
            # # 图片url
            # img_url: str
            # # imgPaths前缀
            # img_prefix: str
            # # 图片路径，多个分隔
            # img_paths: str
            # # 省份
            # province: str
            # # 城市
            # city: str
            # # 县
            # county: str

            # 拍卖网站 标识符 可以是域名
            website = self.website

            # 拍卖类型
            assets_type = ""
            if "车" in assets_name:
                assets_type = self.jidongche
            else:
                assets_type = self.wuzishebei

            # # 关注数
            # onlookers: str
            # # 状态
            # state: str
            # 拍卖链接
            url = i.find_element(By.XPATH, './/a[1]').get_attribute('href')
            # sync_uat: bool = False
            # sync_prd: bool = False

            # 解析详细信息，入库用
            auction_info = Auction_Info(
                origin_id=origin_id,
                auction_id=auction_id,
                assets_name=assets_name,
                announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
                announcement_end_time=str_to_y_m_d_H_M_S(announcement_end_time),
                website=website,
                # province="四川",
                # img_url=img_url,
                # state=state[0],
                assets_type=assets_type,
                url=url
            )
            auction_infos.append(auction_info)

        return auction_infos

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        driver = kwargs.get("driver")
        auction_info = kwargs.get("auction_info")

        time.sleep(2)

        a = driver.find_element(By.XPATH,
                                '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/p[2]/span[2]').text

        import cpca
        df = cpca.transform([a])  # 将cut参数设置为False，只返回市和省信息
        df = df[['市', '省']]  # 仅保留市和省列
        # print(df["省"].values)

        auction_info.province = df["省"].values[0]
        auction_info.city = df["市"].values[0]

        if not auction_info.province:
            auction_info.province = "四川省"

        if not auction_info.city:
            auction_info.city = ""

        auction_info.state = driver.find_element(By.XPATH,
                                                 '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/p[4]/span[2]').text

        details = []
        title = "采购品信息"
        content = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]').get_attribute("outerHTML")
        data_dict = {}
        data_dict["title"] = title
        data_dict["content"] = content.replace(" ", "").replace("\n", "")
        details.append(data_dict)

        title = "项目说明"
        content = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[3]').get_attribute("outerHTML")
        data_dict = {}
        data_dict["title"] = title
        data_dict["content"] = content.replace(" ", "").replace("\n", "")
        details.append(data_dict)

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=details)

    def action(self, *args, **kwargs):
        minpage = 1
        maxpage = 20  # 写死20

        logtool.info("开始爬取")
        logtool.info("进入网页")

        urls = ["https://www.longdaoyun.com/search/business-opportunity/type-caigou-notice.html",
                "https://www.longdaoyun.com/search/business-opportunity/type-zhaobiao-notice.html",
                "https://www.longdaoyun.com/search/business-opportunity/type-jingjia-notice.html",
                "https://www.longdaoyun.com/search/business-opportunity/type-paimai-notice.html"]

        driver = None
        for url in urls:
            driver = self.data_list(url=url)

            while minpage < maxpage:
                # 进行列表处理
                auction_infos = self.parse_data_list(driver=driver)

                # 详情页处理
                for auction_info in auction_infos:
                    driver = self.data_details(url=auction_info.url)
                    time.sleep(3)

                    try:
                        auction_info, auction_datails = self.parse_data_details(driver=driver,
                                                                                auction_info=auction_info)

                        id = self.insert_one_auction_info(auction_info.to_json())
                        auction_datails.id = id
                        self.insert_one_auction_detail(auction_datails.to_json())
                        print(auction_info)
                        print(auction_datails)
                    except Exception as e:
                        continue

                    print(auction_info)

                # 翻页
                driver = self.data_list(url=urls[0])
                driver.find_element(By.XPATH, '//*[@id="layui-laypage-1"]/span[3]/input').send_keys(minpage)
                time.sleep(2)
                driver.find_element(By.XPATH, '//*[@id="layui-laypage-1"]/span[3]/button').click()
                time.sleep(5)

                minpage += 1

        driver.quit()


if __name__ == '__main__':
    wk = Wk()
    wk.action()
