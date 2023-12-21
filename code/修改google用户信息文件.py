import random

from DrissionPage import ChromiumPage, ChromiumOptions


def main(path, path1):
    # 创建多个配置对象，每个指定不同的端口号和用户文件夹路径
    do1 = ChromiumOptions().set_paths(local_port=9111, user_data_path=path)
    do2 = ChromiumOptions().set_paths(local_port=9222, user_data_path=path1)

    # 创建多个页面对象
    page1 = ChromiumPage(addr_driver_opts=do1)
    page2 = ChromiumPage(addr_driver_opts=do2)

    # 每个页面对象控制一个浏览器
    page1.get('https://www.baidu.com')
    page2.get('https://www.baidu.com')


if __name__ == '__main__':
    import shutil

    # 生成一个四位数的随机整数
    n = random.randint(1000, 9999)

    # 定义源文件夹和目标文件夹的路径
    src_folder = r"C:\Users\程家俊\AppData\Local\Google\Chrome\User Data"
    dst_folder = fr"C:\Users\程家俊\AppData\Local\Google\Chrome\{n}"

    # 使用shutil模块的copytree函数复制整个文件夹
    shutil.copytree(src_folder, dst_folder)

    main(src_folder, dst_folder)

    # 使用 shutil.rmtree() 函数删除目录及其所有文件和子目录
    shutil.rmtree(dst_folder)
