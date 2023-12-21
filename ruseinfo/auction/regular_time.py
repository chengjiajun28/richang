import os
import sys

from ruseinfo.auction import logtool
from ruseinfo.auction.main_code import Wk

# 将文件的上级目录添加到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    from datetime import datetime

    # 获取当前时间
    current_time = datetime.now()

    # 格式化当前时间
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    print("当前时间：", formatted_time)

    logtool.info(f"时间：{formatted_time}，启动程序成功！！！")

    wk = Wk()

    wk.action()

    logtool.info("程序入库完成！！！")


def main():
    print("程序开始！！！")

    # 创建一个调度器
    scheduler = BlockingScheduler()

    # 定义定时任务，每隔三十分钟执行一次
    scheduler.add_job(job, 'interval', minutes=25)

    # 启动调度器
    scheduler.start()


if __name__ == '__main__':
    main()
