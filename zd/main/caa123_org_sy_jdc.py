import time

import pandas as pd

from zd.Template import Template


def main():
    website = "caa123_org_sy_jdc"

    df = pd.DataFrame(
        columns=['详情页标题', '地区', "x详情页信息", "结束时间", 'x重要提示', '页面网址'])

    url = "https://paimai.caa123.org.cn/pages/lots/list.html?&status=0&attribute=&term=&startTimeStamp=&endTimeStamp=&standardType=5&canLoan=&isRestricted=&insuranceSupport="

    tp = Template()
    page, path = tp.get_page_obj(url=url)

    time.sleep(5)

    n = 0

    try:

        for i in range(5):

            time.sleep(2)
            datas = page.eles('x:/html/body/div[3]/div/div[2]/div/ul/li')

            for mov1 in datas:
                # 进入详情页点击对象
                title_obj = mov1.ele('x:.//a/p')

                # 获取列表页数据
                time_text = mov1.ele('x:.//a/div[2]/div/p[1]/span[2]').text

                # 点进详情页
                title_obj.click()

                # 切换标签页
                a = page.get_tab(page.latest_tab)
                time.sleep(2)

                # 停止页面加载
                # a.run_cdp('Page.stopLoading')

                for b in range(1, 5):
                    time.sleep(1)
                    a.scroll.to_location(300, 3000 * b)

                time.sleep(1)

                title_text = a.ele('x://*[@id="pro_bid_name"]').text
                diqu = a.ele('x://*[@id="page"]/div[2]/div[1]/div/div[2]/div[15]/span').text

                x重要提示 = a.ele('x://*[@id="DetailTabMain"]/div[1]/div[2]').html

                a.ele('x:/html/body/div[11]/div/div/div[1]/ul/li[2]').click()
                time.sleep(2)

                x详情页信息 = a.ele('x://*[@id="NoticeDetail"]/div[2]').html

                页面网址 = a.url

                # 删除标签页
                tabs = page.tabs
                page.close_tabs(tabs[0])

                print(title_text)
                n += 1

                df.loc[n] = [title_text, diqu, x详情页信息, time_text, x重要提示, 页面网址]

            page.ele('x:/html/body/div[4]/div/div/a[last()]').click()

            page.wait.load_start()

    except Exception as e:
        print(e)

    finally:
        tp.quit_page(page=page, dst_folder=path)
        df.to_csv(f'../csv/{website}.csv', index=False, mode="w")


if __name__ == '__main__':
    main()
