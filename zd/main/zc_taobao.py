import time

import pandas as pd

from zd.Template import Template


def main():
    website = "zc_taobao"

    df = pd.DataFrame(
        columns=["image", '详情页标题', '保证金', '地区', "x详情页物介绍", "x竞买公告", "x竞买须知", "x尾款支付说明",
                 '页面网址'])

    url = "https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?disableNav=YES&page=1&spm=a2129.27064540.puimod-zc-focus-2021_2860107850.category-2-2&pmid=0521799659_1699430115901&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.category-2-2&path=27064540&statusOrders=[%221%22]"

    tp = Template()
    page, path = tp.get_page_obj(url=url)

    time.sleep(5)

    # 停止页面加载
    page.run_cdp('Page.stopLoading')

    n = 0

    try:

        for i in range(5):

            time.sleep(2)
            datas = page.eles('x://*[@id="guid-2004318340"]/div/div/div')
            #                    //*[@id="guid-2004318340"]/div/div/div[1]/a/div[2]/div[1]/span

            for mov1 in datas:
                # 进入详情页点击对象
                title_obj = mov1.ele('x:.//a/div[1]/img')

                # 获取列表页数据
                image = mov1.ele('x:.//a/div[2]/div[1]/span').link

                # 点进详情页
                title_obj.click()

                # 切换标签页
                a = page.get_tab(page.latest_tab)
                time.sleep(2)

                # 停止页面加载
                # a.run_cdp('Page.stopLoading')

                for b in range(1, 7):
                    time.sleep(1)
                    a.scroll.to_location(300, 3000 * b)

                time.sleep(3)

                title_text = a.ele('x://*[@id="page"]/div[4]/div/div/h1').text
                保证金 = a.ele('x://*[@id="J_HoverShow"]/tr[1]/td/span[2]/span').text
                地区 = a.ele('x://*[@id="itemAddress"]').text
                x详情页物介绍 = a.ele('x://*[@id="J_desc"]').html
                x竞买公告 = a.ele('x://*[@id="J_NoticeDetail"]').html
                x竞买须知 = a.ele('x://*[@id="J_ItemNotice"]').html
                x尾款支付说明 = a.ele('x://*[@id="J_CasePayInfo"]/div[2]').html

                页面网址 = a.url

                # 删除标签页
                tabs = page.tabs
                page.close_tabs(tabs[0])

                print(title_text)
                n += 1

                df.loc[n] = [image, title_text, 保证金, 地区, x详情页物介绍, x竞买公告, x竞买须知, x尾款支付说明,
                             页面网址]

            page.ele('x://*[@id="guid-2708524060"]/div/div[2]').click()

            page.wait.load_start()

    except Exception as e:
        print(e)

    finally:
        tp.quit_page(page=page, dst_folder=path)
        df.to_csv(f'../csv/{website}.csv', index=False, mode="w")


if __name__ == '__main__':
    main()
