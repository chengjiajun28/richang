import random
import time

from zd.Template import Template


def zc_taobao():
    tp = Template()

    url = "https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?disableNav=YES&page=1&spm=a2129.27064540.puimod-zc-focus-2021_2860107850.category-2-2&pmid=0521799659_1699430115901&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.category-2-2&path=27064540&statusOrders=[%221%22]"

    page, path = tp.get_page_obj(url=url)

    time.sleep(2)

    page.refresh()  # 刷新页面

    n = 0

    try:
        for i in range(5):

            datas = page.eles('x://*[@id="guid-2004318340"]/div/div/div')
            # '//*[@id="guid-2004318340"]/div/div/div[1]/a/div[1]/img'

            for mov1 in datas:

                image = mov1.ele('x:.//a/div[1]/img').link
                # '//*[@id="guid-2004318340"]/div/div/div[2]/a/div[1]/img'

                title_obj = mov1.ele('x:.//a/div[2]/div[1]/span')

                title_obj_text = title_obj.text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")

                # if title_obj_text == tp.select_mysql_websites(website=website):
                #     return
                #
                # if n == 0:
                #     tp.modify_mysql_websites(website=website, data=title_obj_text)

                title_obj.click()

                time.sleep(random.randint(1, 5))

                a = page.get_tab(page.latest_tab)

                time.sleep(3)

                for b in range(1, 7):
                    time.sleep(1)
                    a.scroll.to_location(300, 3000 * b)

                time.sleep(3)

                title_text = a.ele('x://*[@id="page"]/div[4]/div/div/h1').text
                保证金 = a.ele('x://*[@id="J_HoverShow"]/tr[1]/td/span[2]/span').text
                地区 = a.ele('x://*[@id="J_ItemDetailContent"]/div[last()]').text
                x详情页物介绍 = a.ele('x://*[@id="J_desc"]').html
                x竞买公告 = a.ele('x://*[@id="J_NoticeDetail"]').html
                x竞买须知 = a.ele('x://*[@id="J_ItemNotice"]').html
                x尾款支付说明 = a.ele('x://*[@id="J_CasePayInfo"]/div[2]').html

                页面网址 = a.url

                tabs = page.tabs
                page.close_tabs(tabs[0])

                # 添加几行数据
                df.loc[n] = [image, title_text, 保证金, 地区, x详情页物介绍, x竞买公告, x竞买须知, x尾款支付说明,
                             页面网址]

                n += 1

            # 获取下一页按钮，有就点击
            btn = page('>', timeout=2)
            btn.click()
            page.wait.load_start()

    except Exception as e:
        pass

    finally:

        tp.quit_page(page=page, dst_folder=path)

        return df


if __name__ == '__main__':
    import pandas as pd

    website = "zc_taobao"

    # 创建一个空的DataFrame
    df = pd.DataFrame(
        columns=["image", '详情页标题', '保证金', '地区', "x详情页物介绍", "x竞买公告", "x竞买须知", "x尾款支付说明",
                 '页面网址'])

    # zc_taobao()

    try:

        zc_taobao()

    except Exception as e:
        print(e)

    finally:
        df.to_csv(f'{website}.csv', index=False, mode="w")
