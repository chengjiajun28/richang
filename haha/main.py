import time

import pyautogui


def find_location(a):
    target = pyautogui.locateOnScreen(a)

    # 获取目标图片的中心点坐标
    target_x, target_y = pyautogui.center(target)
    # 在屏幕上点击目标图片的中心点
    pyautogui.click(target_x, target_y)

    return pyautogui


def main(website, title):
    path = './1.png'

    a = find_location(path)

    # 让鼠标向右移动500像素
    a.moveRel(100, 0, duration=1)

    # 模拟双击鼠标
    a.doubleClick()

    time.sleep(1)

    # 输入内容
    a.typewrite(website)

    a = find_location('./2.png')

    # 模拟双击鼠标
    a.doubleClick()

    time.sleep(2)

    a = find_location('./3.png')

    # 模拟鼠标点击操作
    a.click()

    time.sleep(2)

    a = find_location('./4.png')

    # 模拟鼠标点击操作
    a.click()

    # 让鼠标向右移动500像素
    a.moveRel(65, 0, duration=1)

    # 模拟鼠标点击操作
    a.click()

    time.sleep(1)

    a = find_location('./5.png')

    # 模拟鼠标点击操作
    a.click()

    time.sleep(1)

    a = find_location('./6.png')

    # 让鼠标向右移动500像素
    a.moveRel(95, 0, duration=1)

    time.sleep(1)

    # 模拟双击鼠标
    a.doubleClick()
    a.click()

    time.sleep(2)

    import pyperclip
    # 将中文文本复制到剪贴板
    pyperclip.copy(title)
    # 模拟粘贴操作
    a.hotkey("ctrl+v")

    time.sleep(2)

    a = find_location('./7.png')

    # 模拟鼠标点击操作
    a.doubleClick()

    time.sleep(2)

    a = find_location('./8.png')

    # 模拟鼠标点击操作
    a.click()

    time.sleep(1)

    a = find_location('./10.png')

    # 模拟鼠标点击操作
    a.click()

    a = find_location('./9.png')


if __name__ == '__main__':
    import pandas as pd

    # 读取csv文件
    data = pd.read_csv('./xawhcq_sw.csv')

    # 读取第一行数据
    first_row = data.iloc[0]

    print(first_row['详情页标题'])

    main(website="xawhcq_sw", title=first_row['详情页标题'])
