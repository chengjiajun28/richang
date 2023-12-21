import threading
import time


def processing_sliders(tab):
    for i in range(2):

        if '请拖动下方滑块' in tab.ele('x://*[@id="baxia-punish"]/div[2]/div/div[1]/div[2]/div').text:

            try:
                if "重试" in tab.ele('x://*[@id="`nc_1_refresh1`"]').text:
                    tab.ele('x://*[@id="`nc_1_refresh1`"]').click()
            except Exception as e:
                pass

        hua = tab.ele('x://*[@id="nc_1_n1z"]')

        hua.drag(260, 0, 2)


def get_tab(url):
    tab1 = page.new_tab(url=url)

    for i in range(5):
        try:
            tab1 = processing_sliders(tab=tab1)
        except Exception as e:
            break

        time.sleep(3)

    tab1.refresh()

    time.sleep(3)

    tab1.close()


if __name__ == '__main__':
    url = 'https://sf.taobao.com/list/0__1.htm?spm=a213w.7398504.filter.1.2bc04fa7ZKgR9u&auction_source=0&st_param=-1&auction_start_seg=-1'

    from DrissionPage import ChromiumPage, ChromiumOptions

    co = ChromiumOptions().use_system_user_path()
    page = ChromiumPage(co)

    # processing_sliders(page)

    page.get(url=url)

    url_datas = []

    # 处理详情页链接
    for i in range(2):

        time.sleep(1)

        datas = page.eles('x:/html/body/div[3]/div[3]/div[3]/ul/li')

        for data in datas:
            url = data.ele('x:.//a').attr("href")

            url_datas.append(url)

        # 判断页面是否有新的数据
        if len(url_datas) % 48 != 0:
            break

        page.ele('x:/html/body/div[3]/div[4]/a[last()]').click()

    for url in url_datas:
        threading.Thread(target=get_tab, args=(url,)).start()

        time.sleep(5)
