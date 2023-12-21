from DrissionPage._pages.chromium_page import ChromiumPage

url = 'https://odds.leisu.com/3in1-4047215'

# 创建对象同时启动浏览器，如果浏览器已经存在，则接管它
page = ChromiumPage()

page.get(url=url)

datas = page.eles('x://*[@id="fcyt"]/div/div[2]/div/div[2]/div/table/thead/tr/th[2]/div/div/div[2]/div')
#                   //*[@id="fcyt"]/div/div[2]/div/div[2]/div/table/tbody/tr[1]/td[2]/canvas

for i in datas:
    # name = i.ele('x:.//td[2]/canvas').text

    print(f"公司名称：{i.text}")
