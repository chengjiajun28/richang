from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys

abs_path = os.path.abspath(__file__)
sys.path.append(abs_path[0:abs_path.find('auction') - 1])
from datetime import datetime
import time
import requests
from lxml.html import etree
import re
import logtool
from auction.Auction import Auction_Info, Auction_Detials
from auction.BaseCrawler import BaseCrawler
from tools import str_to_y_m_d_H_M_S


class KL(BaseCrawler):

    def __init__(self):
        super().__init__()

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,en-GB;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.ccgp.gov.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }

        self.session = requests.Session()  # 创建会话
        self.session.headers.update(self.headers)

    # 列表
    def data_list(self, url, page):  # 单个主页面访问,注意休息
        time.sleep(3)
        get_params = {}  # 不是每个网站都使用param
        get_html = requests.get(url=url, headers=self.headers)
        get_html.encoding = "utf-8"
        return get_html.text

    # 解析列表
    def parse_data_list(self, html_text):  # 解析主页面,这里是打包的东西
        xpath = ''
        # name = k_tools.html_xpath(html_text, xpath)
        # return name

        # "1项目标识,2入库标识,3项目标题,4开始时间,5结束时间,6定金,7图片url,8图片前缀,9图片路径,10省份
        # 11市级名,12县级名,13域名,14物资类别,15围观人数,16项目状态,17详情页链接

    # 请求详情页
    def data_details(self, url):  # 单个子页面访问，注意休息
        time.sleep(3)
        get_html = requests.get(url=url, headers=self.headers)
        get_html.encoding = "utf-8"
        return get_html.text

    # 解析详情页
    def parse_data_details(self, html_text):  # 解析子页面
        xpath = ''
        # name = k_tools.html_xpath(html_text, xpath)
        # return name  # 返回多个值
        # 1项目状态,2围观人数,3详情链接,4公司名称,5详细信息,6价格

    # annex_format={'title':annex_name1[label_one],'url':xpath_annex1111a}
    # annex.append(annex_format)
    # detials_end=[{'title':'详细信息','content':detials},{'title':'附件','content':annex}]
    # annex:也是上面的列表包字典

    # 页数
    def get_total_page(self, args):  # 页数
        pass

    # def action(self):  # 主函数

    def get_current_year(self):
        now = datetime.now()  # 获取当前时间
        year = now.year  # 获取当前年份
        return year

    def action(self):
        edge = self.get_selenium_obj(r'https://www.yunpaiwang.com/#/biaodi')

        # options = webdriver.ChromeOptions()
        # options.binary_location = "D:\Zpython\chrome-win32"  # 指定Chrome浏览器的路径

        # driver = webdriver.Chrome()
        # edge = webdriver.Chrome()
        # edge.maximize_window()

        edge.get(r'https://www.yunpaiwang.com/#/biaodi')
        time.sleep(3)
        edge.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]').click()  # 物资设备
        edge.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[3]/div[2]/div[2]').click()  # 未开始
        page = range(1, 21)
        for page_one in page:
            if page_one == 1:
                pass
            else:
                edge.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div/button[2]').click()
            edge.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            url_img_xpath = edge.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div')
            '//*[@id="app"]/div/div[2]/div/div[3]/div[1]/div[1]/img'
            assets_name = edge.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div/div[2]')
            '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[2]'
            end_time = edge.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div/div[4]/span')
            # print(end_time)
            '//*[@id="app"]/div/div[2]/div/div[3]/div[3]/div[4]/span'
            onlookers = edge.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div/div[5]/div[1]/div')
            '//*[@id="app"]/div/div[2]/div/div[3]/div[7]/div[5]/div[1]/div'
            label = range(len(onlookers))

            year = self.get_current_year()

            for label_one in range(len(onlookers)):  # 取合集的单独元素
                #     url1 = url_img_xpath[label_one].get_attribute('src')  #
                #
                #     assets_name1 = assets_name[label_one].text
                #
                #     end_time1 = end_time[label_one].text
                #     end_time11 = end_time1.split('日')[0]
                #     end_time111 = end_time11.replace('月', '-')
                #     end_time1112 = str(year) + '-' + end_time111
                #
                #     onlookers_one12 = onlookers[label_one].text
                #     onlookers_one1 = k_tools.find_raw_all_numbers(onlookers_one12)
                #     print(onlookers_one1)
                second_url_click = url_img_xpath[label_one]  #

                time.sleep(10)

                second_url_click.click()
                # 获取所有窗口句柄
                window_handles = edge.window_handles

                # 切换到新页面
                edge.switch_to.window(window_handles[-1])  # 进入到子页面
                time.sleep(5)

                # second_url = edge.current_url
                #
                price = edge.find_element(By.XPATH,
                                           '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[4]/div[1]/span').text
                #price1 = k_tools.find_raw_all_numbers(price)
                print(price)
                #price11 = price1.split('.')[0]
                #print(price11)
                #
                # deposite = edge.find_element(By.XPATH,
                #                              '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[4]/div[2]/span').text
                # # deposite1 = k_tools.find_raw_all_numbers(deposite)
                # # deposite11 = int(deposite1) / 100
                #
                # url_path_end = []
                # url_path = edge.find_elements(By.XPATH,
                #                               '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/img')  # 多个
                # for url_path_one in url_path:
                #     url_path_one1 = url_path_one.get_attribute('src')
                #     url_path_end.append(url_path_one1)
                # url_path_end2 = [url_path_end2_one.split('.com/')[1] for url_path_end2_one in url_path_end]
                # url_path_end1 = ';'.join(url_path_end2)
                #
                # url_prefi = 'https://oss.yunpaiwang.com/'
                #
                # gonggao = edge.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[4]/div[1]/div[3]').click()
                # edge.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # gonggao_xpath = edge.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[4]/div[2]')
                # gonggao_source = gonggao_xpath.get_attribute('outerHTML')
                #
                # company_title = edge.find_element(By.XPATH,
                #                                   '//*[@id="app"]/div/div[2]/div[1]/div[2]/div[2]/div[1]').text
                # company_title1 = company_title.split('企业：')[1]  # 拍卖河北云拍拍卖有限公司
                #
                # province = edge.find_element(By.XPATH,
                #                              '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[4]/div[12]/span').text
                # # province1 = k_tools.match_address_province(province)
                #
                # # annex_format={'title':annex_name1[label_one],'url':xpath_annex1111a}
                # # annex.append(annex_format)
                # # detials_end=[{'title':'详细信息','content':detials},{'title':'附件','content':annex}]
                # origin_id = int(time.time())
                # auction_id = 'yunpai_' + str(origin_id)
                # #
                # # print(url1, assets_name1, end_time1112, onlookers_one1, second_url, price11, deposite11,
                # #       url_path_end1, url_prefi, company_title1, province1)  #gonggao_source
                # # img_urm, auction_titlem, end_timem, onlookersm, second_urlm, pricem, depositm, img_pathm, img_prefim, company_titlem, provincem = url1, assets_name1, end_time1112, onlookers_one1, second_url, price11, deposite11, url_path_end1, url_prefi, company_title1, province1
                # domain = 'yunpaiwang'
                # auction_state = '进行中'
        #         detials = gonggao_source
        #         print(origin_id, auction_id, auction_titlem, end_timem, depositm, img_urm, img_prefim, img_pathm,
        #               provincem, domain, onlookersm, auction_state, second_url
        #               )
        #         auction_info = Auction_Info(origin_id=origin_id, auction_id=auction_id, assets_name=auction_titlem,
        #                                     announcement_end_time=end_timem, deposit=depositm, img_url=img_urm,
        #                                     img_prefix=img_prefim, img_paths=img_pathm, province=provincem,
        #                                     website=domain,
        #                                     assets_type="物资设备", onlookers=onlookersm, state=auction_state,
        #                                     url=second_urlm)
        #         auction_info_id = self.insert_one_auction_info(auction_info.to_json())
        #         logtool.info("基础数据导入成功")
        #         print(auction_state, onlookersm, second_urlm, company_titlem, pricem
        #               )  # detials,
        #         auction_detials = Auction_Detials(state=auction_state, onlookers=onlookersm, url=second_urlm,
        #                                           tendering_org=company_title, detials=detials, start_price=pricem,
        #                                           id=auction_info_id)
        #         self.insert_one_auction_detail(auction_detials.to_json())
        #         logtool.info("详细数据导入成功")
        #
                edge.switch_to.window(window_handles[0])
        #         time.sleep(5)
        #
        # edge.quit()


if __name__ == '__main__':
    # "1项目标识,2入库标识,3项目标题,4开始时间,5结束时间,6定金,7图片url,8图片前缀,9图片路径,10省份
    # 11市级名,12县级名,13域名,14物资类别,15围观人数,16项目状态,17详情页链接

    # 1项目状态,2围观人数,3详情链接,4公司名称,5详细信息,6价格

    # all_value = (1,2,3,5,6,7,8,9,10,13,14,15,16,17)  # 13
    # second_all_value = (1,2,3,4,5,6)
    # str = k_tools.format_sql(all_value, second_all_value)
    # print(str[0])
    # print(str[1])
    operation = KL()
    operation.action()
