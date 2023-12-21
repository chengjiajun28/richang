import random
import shutil
import time

import pymysql
from DrissionPage import ChromiumPage, ChromiumOptions


# # 导入 ChromiumOptions
# from DrissionPage import ChromiumPage, ChromiumOptions
#
# # 创建浏览器配置对象，指定浏览器路径
# co = ChromiumOptions().set_paths(browser_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
# # 用该配置创建页面对象
# page = ChromiumPage(addr_driver_opts=co)


class Template:

    def __init__(self):
        super().__init__()

    def init_page(self):
        do1 = ChromiumOptions().set_paths(local_port=random.randint(1000, 9999))
        page = ChromiumPage(addr_driver_opts=do1)

        return page

    def get_page_obj(self, url):

        # 创建浏览器对象
        page1, path = self.init_page()

        page1.get(url=url, interval=3)  # 获取网页

        return page1

    def modify_mysql_websites(self, website, data):
        # 连接MySQL数据库
        connection = pymysql.connect(
            host='118.195.246.81',  # 服务器IP地址
            port=3406,  # 端口号
            user='root',  # 数据库的用户名
            password='ruse#@!2022r',  # 数据库的密码
            database='datas',  # 数据库名称
        )

        # 创建游标
        cursor = connection.cursor()

        # 执行修改操作
        sql = f"UPDATE websites SET 参考数据='{data}' WHERE 域名='{website}'"
        cursor.execute(sql)

        # 提交更改
        connection.commit()

        # 输出受影响的行数
        print(cursor.rowcount, "record(s) affected")

        # 关闭数据库连接
        connection.close()

    def select_mysql_websites(self, website):
        connection = pymysql.connect(
            host='118.195.246.81',
            port=3406,
            user='root',
            password='ruse#@!2022r',
            database='datas',
        )

        cursor = connection.cursor()

        # 执行查询语句
        sql = f"SELECT 参考数据 FROM websites WHERE 域名 = '{website}';"
        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result[0][0]

    # 创建配置文件
    def copy_configuration(self):
        # 生成一个四位数的随机整数
        n = random.randint(1000, 9999)

        # 定义源文件夹和目标文件夹的路径
        src_folder = r"C:\Users\程家俊\AppData\Local\Google\Chrome\User Data"
        dst_folder = fr"C:\Users\程家俊\AppData\Local\Google\Chrome\{n}"

        # 使用shutil模块的copytree函数复制整个文件夹
        shutil.copytree(src_folder, dst_folder)

        return dst_folder

    # 删除配置文件
    def delete_configuration(self, dst_folder):

        # 使用 shutil.rmtree() 函数删除目录及其所有文件和子目录
        shutil.rmtree(dst_folder)

    # 关闭浏览器，删除配置文件
    def quit_page(self, page, dst_folder):
        page.quit()

        time.sleep(5)

        self.delete_configuration(dst_folder)

    def run(self, data, df, tp, page, path):
        try:

            data

        except Exception as e:
            print(e)

        finally:

            return df, tp, page, path


if __name__ == '__main__':
    tp = Template()

    a = tp.select_mysql_websites(website='ouyeel_jj')

    print(a)
