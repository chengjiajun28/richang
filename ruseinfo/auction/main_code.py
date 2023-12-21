import os
import sys

# 将文件的上级目录添加到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
from datetime import datetime, timedelta
import jionlp
import pandas as pd
import pymysql

from ruseinfo.auction import logtool
from ruseinfo.auction.Auction import Auction_Detials, Auction_Info
from ruseinfo.auction.BaseCrawler import BaseCrawler
from ruseinfo.auction.handle_details import handle
from ruseinfo.tools import str_to_y_m_d_H_M_S


def select_mysql_websites():
    connection = pymysql.connect(
        host='118.195.246.81',
        port=3406,
        user='root',
        password='ruse#@!2022r',
        database='datas',
    )

    cursor = connection.cursor()

    # 执行查询语句
    sql = f"SELECT * FROM websites"
    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


class Wk(BaseCrawler):
    def __init__(self):
        super().__init__()

    # 请求列表
    def data_list(self, *args, **kwargs):
        pass

    # 请求详情页
    def data_details(self, *args, **kwargs):
        pass

    def get_total_page(self, *args, **kwargs):
        pass

    # 解析列表
    def parse_data_list(self, *args, **kwargs):
        global a
        row = kwargs.get("row")
        field_names = kwargs.get("field_names")
        website = kwargs.get("website")

        # 网站原始id
        # origin_id: str
        origin_id = None

        origin_id = str(time.time())

        # 拍卖标的ID
        # auction_id: str
        auction_id = None

        auction_id = f"{self.website}_{origin_id}"

        # 拍卖公告名称
        # assets_name: str
        assets_name = None
        try:
            assets_name = row["详情页标题"].replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")


        except Exception as e:
            auction_info = 0

            return auction_info

        # 处理时间
        announcement_start_time = None
        announcement_end_time = None

        # 第一种时间情况
        try:

            time_one = jionlp.parse_time(row['起止日期'])

            # 报名开始时间
            # announcement_start_time: str
            announcement_start_time = str_to_y_m_d_H_M_S(time_one['time'][0])

            # 报名截止时间
            # announcement_end_time: str
            announcement_end_time = str_to_y_m_d_H_M_S(time_one['time'][1])

        except Exception as e:
            pass

        # 第二种时间情况
        try:

            try:
                # 报名开始时间

                time_one = jionlp.parse_time(row['开始时间'])
                announcement_start_time = str_to_y_m_d_H_M_S(time_one['time'][0])
            except Exception as e:
                # 获取当前时间
                now = datetime.now()

                # 将时间格式化为字符串
                formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

                announcement_start_time = str_to_y_m_d_H_M_S(formatted_now)

            # 报名截止时间

            time_one = jionlp.parse_time(row['结束时间'])
            announcement_end_time = str_to_y_m_d_H_M_S(time_one['time'][0])

        except Exception:
            # 获取当前时间
            now = datetime.strptime(announcement_start_time, "%Y-%m-%d %H:%M:%S")

            # 将时间加上 30 天
            end_time = (now + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

            announcement_end_time = str_to_y_m_d_H_M_S(end_time)

        # 状态
        # state: str
        state = ""
        try:
            state = row["状态"]
        except Exception as e:
            state = ""

        # 保证金
        deposit = ""
        try:
            string = row['保证金'].replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "").split('.')[0]

            deposit = jionlp.parse_money(string)["num"]

        except Exception as e:
            deposit = ""
            # print('保证金出错！！！')

        # 图片url
        # img_url: str
        img_url = None
        try:
            img_url = row["图片网址"]
            if not img_url.startswith("https") and not img_url.startswith("http"):
                img_url = "https:" + img_url
        except Exception as e:
            img_url = ""
            # print("图片网址出错！！！")

        if len(img_url) > 255:
            img_url = ""

        # imgPaths前缀
        # img_prefix: str

        # 图片路径，多个分隔
        # img_paths: str
        img_paths = img_url

        for field_name in field_names:
            if pd.isnull(row[field_name]):
                continue

            if "详情页图片" in field_name:
                img_paths += row[field_name] + ";"

        # 省份
        # province: str

        try:
            diqu = jionlp.parse_location(row["地区"])
            province = diqu.get("province")
        except Exception as e:
            diqu = jionlp.parse_location(assets_name)
            province = diqu.get("province")

        if not province:

            try:
                diqu = jionlp.parse_location(website[11])
                province = diqu.get("province")
            except Exception as e:
                province = ""

        if not province:
            diqu = jionlp.parse_location(assets_name)
            province = diqu.get("province")

        if not province:
            province = "四川省"

        # 城市
        # city: str
        city = diqu.get("city")

        # 县
        # county: str
        county = diqu.get("county")

        # 拍卖类型
        # assets_type: str
        assets_type = None

        # 关注数
        onlookers = None
        try:
            string = row["关注数"].replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
            # 使用正则表达式提取所有的数字
            onlookerss = re.findall(r'\d+', string)
            onlookers = ''.join(f'{num}' for num in onlookerss)

        except Exception:
            onlookers = ""
            # print('关注数出错')

        # 拍卖链接
        # url: str
        url = row["页面网址"]

        # 解析详细信息，入库用
        auction_info = Auction_Info(
            origin_id=origin_id,
            auction_id=auction_id,
            assets_name=assets_name,
            announcement_start_time=str_to_y_m_d_H_M_S(announcement_start_time),
            announcement_end_time=str_to_y_m_d_H_M_S(announcement_end_time),
            deposit=deposit,
            img_url=img_url,
            img_paths=img_paths,
            province=province,
            city=city,
            county=county,
            website=self.website,
            state=state,
            onlookers=onlookers,
            assets_type=assets_type,
            url=url
        )

        return auction_info

    # 解析详情页
    def parse_data_details(self, *args, **kwargs):
        row = kwargs.get("row")
        auction_info = kwargs.get("auction_info")
        field_names = kwargs.get("field_names")

        detials = []
        for field_name in field_names:
            if pd.isnull(row[field_name]):
                continue

            if "x" in field_name:
                detial = {
                    "title": field_name,
                    "content": row[field_name]
                }

                detials.append(detial)

        if len(detials) == 1:
            for field_name in field_names:
                if pd.isnull(row[field_name]):
                    continue

                if "x" in field_name:
                    detials = row[field_name]

        if len(detials) == 0:
            a = 1
            b = 0

            return a, b

        return auction_info, Auction_Detials(state=auction_info.state,
                                             url=auction_info.url, detials=detials)

    def action(self, *args, **kwargs):

        from datetime import datetime

        # 获取当前时间
        current_time = datetime.now()

        # 格式化当前时间
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        logtool.info(f"当前时间：f{formatted_time}")

        # 获取域名
        websites = select_mysql_websites()

        # 获取所有数据给判断判重用
        data = self.select_mysql_data()

        # 获取分类数据
        mysql_classification = self.select_mysql_classification()

        # 遍历域名
        for i, website in enumerate(websites):

            self.website = website[2]

            # 数据入库成功：n  关键词筛除：g 筛选词筛出：y 没有标题：m  数据重复：s  详情页为空：x  失败：b

            n = 0
            m = 0
            s = 0
            x = 0
            b = 0
            p = 0
            time_fail = 0

            # 判断是否上线
            if not website[3]:
                continue

            self.website = website[2]

            # 读取CSV文件
            try:
                file_path = f"./csv/{website[2]}.csv"
                # file_path = f"C:/Users/程家俊/Desktop/csv/{website[2]}/{website[2]}.csv"

                dfs = pd.read_csv(file_path)  # f"C:/Users/程家俊/Desktop/csv/{website[2]}/{website[2]}.csv"


            except Exception as e:

                continue

            # 处理详情页信息
            # dfs = handle(website=website[2], dfs=dfs)

            # 处理数据

            # 遍历数据

            for _, row in dfs.iterrows():  # 取表格每行

                # 处理列表信息
                try:

                    auction_info = self.parse_data_list(row=row, field_names=dfs.columns.tolist(), website=website)

                except Exception as e:

                    b += 1

                    continue

                # 判断标题是否有问题
                if auction_info == 0:
                    m += 1

                    continue

                # 处理详情页
                try:

                    # 处理详情页的数据，html
                    row = handle(website=website[2], row=row)

                    auction_info, auction_detial = self.parse_data_details(row=row, auction_info=auction_info,
                                                                           field_names=dfs.columns.tolist())

                except Exception as e:

                    p += 1

                    continue

                # 判断详情页是否为空
                if auction_info == 1:
                    x += 1

                    continue

                # 去重

                start_time = datetime.strptime(auction_info.announcement_start_time, "%Y-%m-%d %H:%M:%S").replace(
                    hour=0, minute=0, second=0)
                end_time = datetime.strptime(auction_info.announcement_end_time, "%Y-%m-%d %H:%M:%S").replace(hour=0,
                                                                                                              minute=0,
                                                                                                              second=0)

                # try:
                #     if 1 in [1 if i[3] == auction_info.assets_name and (
                #             start_time == i[2].replace(hour=0, minute=0, second=0)
                #             or
                #             end_time == i[1].replace(hour=0, minute=0, second=0)
                #     ) else 0 for i in data]:
                #         s += 1
                #
                #         continue
                # except Exception as e:
                #     time_fail += 1
                #     continue

                # if self.mysql_query(assets_name=auction_info.assets_name,
                #                     announcement_start_time=auction_info.announcement_start_time):
                #     s += 1
                #
                #     continue
                #
                # if self.mysql_query(assets_name=auction_info.assets_name,
                #                     announcement_end_time=auction_info.announcement_end_time):
                #     s += 1
                #
                #     continue

                # 筛选分类

                auction_info.assets_type = "其它"
                for haha in mysql_classification:
                    # 判断需要的筛选词是否为空
                    if not haha[0]:
                        continue

                    # 判断需要的筛选词是否为空
                    if not haha[1]:
                        continue

                    # 移除列表中的空格
                    words_list = [word for word in haha[1].split(',') if word != '']

                    # 筛选不要的
                    if haha[2]:
                        # 移除列表中的空格
                        words_list1 = [word1 for word1 in haha[2].split(',') if word1 != '']

                        if any(i in auction_info.assets_name for i in words_list1):
                            continue

                    if any(i in auction_info.assets_name for i in words_list):
                        auction_info.assets_type = haha[0]

                        break

                # 入库
                id = self.insert_one_auction_info(auction_info.to_json())
                auction_detial.id = id
                self.insert_one_auction_detail(auction_detial.to_json())

                n += 1

            logtool.info(
                f'\n---------域名：{i, website[2]}，数据入库成功：{n}，列表页解析失败：{b}，时间问题：{time_fail}，详情页解析失败：{p}，没有标题：{m}，数据重复：{s}，详情页为空：{x}，')


if __name__ == '__main__':
    wk = Wk()

    wk.action()
