import time

import pandas as pd
import pyautogui

# 图片文件名和坐标信息
image_info = {
    '1.png': (100, 0),
    '2.png': (0, 0),
    '3.png': (0, 0),
    '4.png': (0, 0),
    '5.png': (0, 0),
    '6.png': (0, 0),
    '7.png': (0, 0),
    '8.png': (0, 0),
    '9.png': (0, 0),
    '10.png': (0, 0)
}


def click_image(image_name):
    target = pyautogui.locateOnScreen(image_name)
    if target:
        target_x, target_y = pyautogui.center(target)
        pyautogui.click(target_x, target_y)
        return True
    else:
        return False


def main(website, title):
    try:
        for image_name, move_offset in image_info.items():
            if click_image(image_name):
                if move_offset != (0, 0):
                    pyautogui.moveRel(move_offset[0], move_offset[1], duration=1)
                if '输入内容' in image_name:
                    pyautogui.typewrite(website if 'website' in image_name else title)
                time.sleep(2)
            else:
                print(f'未找到目标图片 {image_name}')
                break
    except Exception as e:
        print('发生异常:', e)


if __name__ == '__main__':
    data = pd.read_csv('./ggzy_xzsp_changzhou_gov_gc.csv')
    first_row = data.iloc[0]
    print(first_row['详情页标题'])
    main(website="ggzy_xzsp_changzhou_gov_gc", title=first_row['详情页标题'])
