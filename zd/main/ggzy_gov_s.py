import time

from zd.Template import Template


def ggzy_gov_s(df):
    tp = Template()

    url = "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp"

    page, path = tp.get_page_obj(url=url)

    time.sleep(2)
    print(1)
    while True:
        try:

            time.sleep(2)
            page.ele('x://*[@id="choose_stage_0001"]/a').click()

            break
        except:
            page.ele('x://*[@id="proceed-button"]').click()

    time.sleep(2)

    # 停止页面加载
    page.run_cdp('Page.stopLoading')

    time.sleep(2)

    page.ele('x://*[@id="searchButton"]').click()

    n = 0

    time.sleep(5)

    try:

        for i in range(5):

            time.sleep(2)
            datas = page.eles('x://*[@id="toview"]/div')

            for mov1 in datas:
                title_obj = mov1.ele('x:.//div/h4/a')

                diqu = mov1.ele('x:.//div/p/span[2]').text

                # if title_obj_text == tp.select_mysql_websites(website=website):
                #     return

                # if n == 0:
                #     tp.modify_mysql_websites(website=website, data=title_obj_text)

                title_obj.click()

                a = page.get_tab(page.latest_tab)

                time.sleep(2)

                title_text = a.ele('x:/html/body/div[5]/h4').text
                time_text = a.ele('x://*[@id="div_0101"]/ul/li[1]/span').text

                x详情页信息 = a.ele('x://*[@id="mycontent"]').html

                tabs = page.tabs
                page.close_tabs(tabs[0])

                print(title_text)

                n += 1

                df.loc[n] = [title_text, diqu, x详情页信息, time_text]

            btn = page('下一页', timeout=2)
            btn.click()
            page.wait.load_start()

    except Exception as e:
        print(e)

    finally:

        return df, tp, page, path


def main():
    global tp, page, path
    import pandas as pd

    website = "ggzy_gov_s"

    # 创建一个空的DataFrame
    df = pd.DataFrame(
        columns=['详情页标题', '地区', "x详情页信息", "开始时间"])

    try:

        df, tp, page, path = ggzy_gov_s(df, )

    except Exception as e:
        print(e)

    finally:
        tp.quit_page(page=page, dst_folder=path)

        df.to_csv(f'{website}.csv', index=False, mode="w")


if __name__ == '__main__':
    # import pandas as pd
    #
    # website = "tuopaishede"
    #
    # # 创建一个空的DataFrame
    # df = pd.DataFrame(
    #     columns=["image", '详情页标题', '保证金', '地区', "x详情页物介绍", "x联系信息"])

    # ouyeel()

    # try:
    #
    #
    # except Exception as e:
    #     print(e)
    #
    # finally:
    #     df.to_csv(f'{website}.csv', index=False, mode="w")

    main()
