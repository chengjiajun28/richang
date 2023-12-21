import random
import time

from zd.Template import Template


def ouyeel():
    tp = Template()

    url = "https://www.ouyeel.com/search-ng/exchange/search/bidding?biddingType=10"

    page= tp.get_page_obj(url=url)

    time.sleep(2)

    n = 0

    # try:
    for i in range(5):

        datas = page.eles('x:/html/body/div/div[2]/div[3]/section/section[2]/div[2]/div[1]/div')

        for mov1 in datas:

            image = mov1.ele('x:.//div[1]/img').link
            # '//*[@id="guid-2004318340"]/div/div/div[2]/a/div[1]/img'

            title_obj = mov1.ele('x:.//div[2]/div[1]/div[1]')

            title_obj_text = title_obj.text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")

            if title_obj_text == tp.select_mysql_websites(website=website):
                return

            if n == 0:
                tp.modify_mysql_websites(website=website, data=title_obj_text)

            title_obj.click()

            time.sleep(random.randint(1, 5))

            a = page.get_tab(page.latest_tab)

            time.sleep(1)

            # 停止页面加载
            # a.run_cdp('Page.stopLoading')

            for b in range(1, 5):
                time.sleep(1)
                a.scroll.to_location(300, 3000 * b)

            time.sleep(1)

            title_text = a.ele('x://*[@id="page-wrapper"]/div[1]/div[2]/div[1]/div[1]/h2').text
            保证金 = a.ele('x://*[@id="showDfyj"]').text
            地区 = a.ele('x://*[@id="tab-1"]/div[2]/div/table/tbody/tr[1]/td[2]').text
            x详情页物介绍 = a.ele('x://*[@id="tab-1"]/div[1]').html
            x联系信息 = a.ele('x://*[@id="tab-1"]/div[2]').html

            页面网址 = a.url

            tabs = page.tabs
            page.close_tabs(tabs[0])

            # 添加几行数据
            df.loc[n] = [image, title_text, 保证金, 地区, x详情页物介绍, x联系信息, 页面网址]

            n += 1

        # 获取下一页按钮，有就点击
        btn = page('›', timeout=2)
        btn.click()
        page.wait.load_start()

    # except Exception as e:
    #     pass
    #
    # finally:
    #
    #     tp.quit_page(page=page, dst_folder=path)
    #
    #     return df


if __name__ == '__main__':
    import pandas as pd

    website = "ouyeel"

    # 创建一个空的DataFrame
    df = pd.DataFrame(
        columns=["image", '详情页标题', '保证金', '地区', "x详情页物介绍", "x联系信息", '页面网址'])

    ouyeel()

    # try:
    #
    #     ouyeel()
    #
    # except Exception as e:
    #     print(e)
    #
    # finally:
    #     df.to_csv(f'{website}.csv', index=False, mode="w")
