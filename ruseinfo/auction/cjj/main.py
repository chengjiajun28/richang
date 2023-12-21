import threading
import time

from DrissionPage._units.actions import Actions


def processing_sliders(tab):
    # 创建动作链对象
    ac = Actions(tab)

    # 左键按住元素
    ac.hold('x://*[@id="nc_1_n1z"]')
    # 向右移动鼠标300像素
    ac.right(260)
    # 释放左键
    ac.release()


def get_tab(tab1):
    # tab1 = page.new_tab(url=url)

    for i in range(5):
        try:
            print(2)
            tab1.ele('x://*[@id="`nc_1_refresh1`"]').click()
            print(1)
        except Exception as e:
            pass

        try:
            tab1 = processing_sliders(tab=tab1)
        except Exception as e:
            break

        time.sleep(3)

    tab1.refresh()


if __name__ == '__main__':
    url = 'https://sf.taobao.com/list/0__1.htm?spm=a213w.7398504.filter.1.2bc04fa7ZKgR9u&auction_source=0&st_param=-1&auction_start_seg=-1'

    from DrissionPage import ChromiumPage, ChromiumOptions

    co = ChromiumOptions().use_system_user_path()
    page = ChromiumPage(co)

    # get_tab(page)

    page.get(url=url)

    url_datas = []

    # 处理详情页链接

    time.sleep(3)

    datas = page.eles('x:/html/body/div[3]/div[3]/div[3]/ul/li')
    #                   //*[@id="guid-2004318340"]/div/div/div[1]/a

    for data in datas:
        url = data.ele('x:.//a').attr("href")

        url_datas.append(url)

    for url in url_datas:
        tab1 = page.new_tab(url=url)

        get_tab(tab1)

        time.sleep(5)

    # for data in page.eles('x:/html/body/div[3]/div[3]/div[3]/ul/li'):
    #     data.ele('x:.//a').click()
    #
    #     tab = page.get_tab(0)
    #
    #     try:
    #         if '请拖动下方滑块' in tab.ele('x://*[@id="baxia-punish"]/div[2]/div/div[1]/div[2]/div').text:
    #             time.sleep(5555)
    #
    #     except Exception as e:
    #
    #         tab.close()
