import base64
import json
from loguru import logger
import requests
import execjs
import time

# cookies = {
#     'SESSION': 'ed238669-3037-4cc0-ab44-9f0e66b5eeca',
#     'amlbcookie': '01',
#     'AMAuthCookie': 'AQIC5wM2LY4SfcygUeomz4A4t758ZF5ntsvjcaH9eDa4G7I.*AAJTSQACMDEAAlNLABQtNjIxNzIyMTE5OTAzMzMyMjQyNQ..*',
# }

headers = {
    'authority': 'iam.pt.ouchn.cn',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'SESSION=ed238669-3037-4cc0-ab44-9f0e66b5eeca; amlbcookie=01; AMAuthCookie=AQIC5wM2LY4SfcygUeomz4A4t758ZF5ntsvjcaH9eDa4G7I.*AAJTSQACMDEAAlNLABQtNjIxNzIyMTE5OTAzMzMyMjQyNQ..*',
    'origin': 'https://iam.pt.ouchn.cn',
    'referer': 'https://iam.pt.ouchn.cn/am/UI/Login?realm=%2F&service=initService&goto=https%3A%2F%2Fiam.pt.ouchn.cn%2Fam%2Foauth2%2Fauthorize%3Fservice%3DinitService%26response_type%3Dcode%26client_id%3D6f05d69dd1a847fe%26scope%3Dall%26decision%3DAllow',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

# 请求方式
requests_session = requests.session()


# 打开js
def read_js_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 使用js解密
def call_str_enc(data, firstKey='OqxQ1Iea4njSROH/N06Tuw==', secondKey=None, thirdKey=None):
    js_code = read_js_code('./dome.js')
    # 创建 JavaScript 环境
    ctx = execjs.compile(js_code)
    # 调用 JavaScript 函数
    encrypted_data = ctx.call("strEnc", data, firstKey, secondKey, thirdKey)

    return encrypted_data


# 返回验证码 打码平台
def get_captcha():
    while True:
        img_url = requests_session.get('https://iam.pt.ouchn.cn/am/validate.code')
        with open('123.png', 'wb') as f:
            f.write(img_url.content)
        img_b64 = base64.b64encode(img_url.content).decode()
        data = {'img': img_b64}
        response = requests_session.post('http://111.230.41.237:56012/one_code', json=data)

        code = response.json().get('code', '0000')
        logger.info(code)
        if code != '0000':
            break
    return code


# 用于验证验证码
def verify_captcha(code):
    img_ver_url = "https://iam.pt.ouchn.cn/am/validatecode/verify.do"
    data = {'validateCode': code}

    response = requests_session.post(url=img_ver_url, data=data, headers=headers)
    return response.json()


# 登录函数
def login(username, password):
    url = "https://iam.pt.ouchn.cn/am/UI/Login"
    img_code = get_captcha()

    captcha_verification_result = verify_captcha(img_code)
    logger.info(f' 验证码识别情况{captcha_verification_result}')

    if captcha_verification_result['state'] == 'success':
        login_data = {
            "IDToken1": call_str_enc(username),
            "IDToken2": call_str_enc(password),
            "IDToken3": img_code,
            "goto": "aHR0cHM6Ly9pYW0ucHQub3VjaG4uY24vYW0vb2F1dGgyL2F1dGhvcml6ZT9zZXJ2aWNlPWluaXRTZXJ2aWNlJnJlc3BvbnNlX3R5cGU9Y29kZSZjbGllbnRfaWQ9NmYwNWQ2OWRkMWE4NDdmZSZzY29wZT1hbGwmZGVjaXNpb249QWxsb3c=",
            "gotoOnFail": "",
            "SunQueryParamsString": "cmVhbG09LyZzZXJ2aWNlPWluaXRTZXJ2aWNlJg==",
            "encoded": "true",
            "gx_charset": "UTF-8",
        }
        response = requests_session.post(url, data=login_data, headers=headers)
        auth_code = str(response.url).split("=")[-1]
        return auth_code

    else:
        logger.info("验证码验证失败")


# 判断登录函数 是否登录成功
def get_token(user, pwd):
    auth_code = login(user, pwd)

    data = {"code": auth_code}

    urls = 'https://ks.ouchn.cn/g/auth/open/studentAuth3'

    response_url = requests_session.post(urls, data=data, headers=headers)

    if response_url.json()['msg'] == "登录成功":
        token = response_url.json()['data']['token']
        return token

    else:
        logger.info("登录失败")


# 得到身份令牌
def get_kisid(user, pwd):
    stu_no_id = {"stuNo": user, "examType": 1}
    url_find_exam_plan_id_by_stu = 'https://ks.ouchn.cn/g/examination/answer/findExamPlanIdByStu'
    headers['token'] = get_token(user, pwd)
    # headers['token'] = 'student4b4x1sA/CJlEXGbYDk51Vzz7KvC+b1G4pRdMh0alwtI='
    response_stu_no_id = requests_session.post(url_find_exam_plan_id_by_stu, data=stu_no_id, headers=headers)

    response_content = response_stu_no_id.json()
    response_stu_no_id_list = response_content.get('data', [])
    if response_stu_no_id_list:
        kisid = response_stu_no_id_list[0]['examPlanId']
        get_exam_scores(user, kisid)
    else:
        # 处理列表为空的情况，例如打印一条消息或执行其他适当的操作
        print("列表为空")
    # 添加延时，隔1秒执行下一次请求
    time.sleep(1)


# 多线程
def get_kisid_parallel(users, passwords):
    with ThreadPoolExecutor(max_workers=500) as executor:  # 设置合适的线程数
        executor.map(get_kisid, users, passwords)


# 处理数据的url链接
def get_exam_scores(user, kisid):
    wand = {"ksId": user, "kdKsjhId": kisid, "size": -1}
    url_cj = 'https://ks.ouchn.cn/g/examination/answer/findExamScore'
    response_url = requests_session.post(url_cj, data=wand, headers=headers)
    response_id_list = response_url.json()['data']['records']

    user_list = []
    list = []
    from datetime import datetime, timedelta
    # 合并所有recorder当中的数据
    global formatted_start_date
    for user_li in response_id_list:
        user_list.append(user_li)

    # 处理试卷链接
    for user_list in user_list:
        # 时间
        if "submitAnswers" in user_list:
            submit_answers_time = datetime.strptime(user_list["submitAnswers"], "%Y-%m-%d %H:%M:%S")
            # 最小时间
            start_date = (submit_answers_time - timedelta(days=32 + 4 * 7 + 365)).date()
            # 转换为2022/5/1
            formatted_start_date = start_date.strftime("%Y/%m/%d").lstrip("0").replace("/0", "/")

        # 路径前面
        testPaperPackageId = user_list["testPaperPackageId"]
        # 路径后面
        testPaperId = user_list["testPaperId"]

        # 如果有链接就不拼接
        testPaperPath = user_list["testPaperPath"]

        # testPaperPath为空的时候返回拼接 不为空就返回未拼接
        if testPaperPath == 0:
            # 返回拼接的部分
            list.append([formatted_start_date, testPaperPackageId, testPaperId])
            # 拼接
            for i in list:
                time_str = i[0]
                packageid = i[1]
                paperid = i[2]

                date_obj = datetime.strptime(time_str, "%Y/%m/%d")
                for _ in range(30):
                    date_obj += timedelta(days=1)
                    updated_time_str = f"{date_obj.year}/{str(int(date_obj.month))}/{str(int(date_obj.day))}"
                    url = f"https://ks.ouchn.cn/asset/exampaper/{updated_time_str}/{packageid}/{paperid}.json"
                    list.append(url)
        else:
            # 未拼接
            url = "https://ks.ouchn.cn/" + testPaperPath
            list.append(url)

    # request_post(list)


# 循环判断url当中的连接
def request_post(list):
    # 破解文字加密链接
    url = 'http://111.230.41.237:7592/api/getPaper'

    # 遍历链接
    json_list = []
    for i in list:
        logger.debug(i)
        json_data = {
            "url": i
        }
        response_url = requests_session.post(url, json=json_data)
        json_list_e = json.loads(response_url.text)['decryptedText']

        json_list.append(json_list_e)

    return get_exam_json(json_list)


def get_exam_json(json_list):
    global proOptionsVos_cont, proOptionsVos_resultType

    liste = []
    # 遍历[当中的json]
    for i in json_list:
        data = json.loads(i)
        # 数据
        # 试卷代码
        number = data['paperName']

        # 处理数据
        for proGroupVoList in data['proGroupVoList']:
            for proVoList in proGroupVoList['proVoList']:
                courseName = proVoList['courseName']
                for proSubVos in proVoList['proSubVos']:
                    proTypeName = proSubVos['proTypeName']
                    cont = proSubVos['cont'].replace("<br/>", "").replace("&nbsp;", "").replace("</p>", "").replace(
                        "<p>",
                        "").replace(
                        "— ", "").replace("—", "").strip()
                    proOptionsVos_cont_list = []
                    proOptionsVos_resultType_list = []
                    if 'proOptionsVos' in proSubVos and proSubVos['proOptionsVos']:
                        for proOptionsVos in proSubVos['proOptionsVos']:
                            if 'cont' in proOptionsVos:
                                proOptionsVos_cont = proOptionsVos['cont'].replace("<br/>", "").replace("&nbsp;",
                                                                                                        "").replace(
                                    "</p>", "").replace("<p>", "").replace("— ", "").replace("—", "").strip()
                                proOptionsVos_cont_list.append(proOptionsVos_cont)
                            if 'resultType' in proOptionsVos:
                                proOptionsVos_resultType = proOptionsVos['resultType']
                                proOptionsVos_resultType_list.append(proOptionsVos_resultType)

                        liste.append(
                            [number, proTypeName, cont, proOptionsVos_cont_list, proOptionsVos_resultType_list,
                             courseName])

                    else:
                        logger.info("没有选项")

    return mysql_list(liste)


# 存放数据库
def mysql_list(liste):
    import mysql.connector
    from datetime import datetime

    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="guojia"
    )

    cursor = db_connection.cursor()

    insert_query = "INSERT INTO your_table (number, proTypeName, cont, proOptionsVos_cont_list, proOptionsVos_resultType_list, courseName, entry_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for item in liste:
        number, proTypeName, cont, proOptionsVos_cont_list, proOptionsVos_resultType_list, courseName = item
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        proOptionsVos_cont_list_str = json.dumps(proOptionsVos_cont_list)
        proOptionsVos_resultType_list_str = json.dumps(proOptionsVos_resultType_list)

        insert_values = (
            number, proTypeName, cont, proOptionsVos_cont_list_str, proOptionsVos_resultType_list_str, courseName,
            current_time)

        cursor.execute(insert_query, insert_values)

    db_connection.commit()
    cursor.close()
    db_connection.close()


# username = "2137106406504"
# password = "Ouchn@19920623"
# get_kisid(username, password)

import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def read_excel(file_path):
    # 从Excel文件中读取数据
    df = pd.read_excel(file_path)
    return df


def main():
    # # 从Excel读取用户名和密码
    # excel_file_path = 'E:\Python_cs\dome_cs\查课数据.xlsx'  # 用实际路径替换
    # df = read_excel(excel_file_path)
    #
    # # 提取账号和密码列
    # usernames = df['账号'].tolist()
    # passwords = df['密码'].tolist()
    #
    # # 逐个传入账号和密码
    # for user, pwd in zip(usernames, passwords):
    #     logger.debug(user)

    user = "2137106406504"
    pwd = "Ouchn@19920623"


    get_kisid(user, pwd)


if __name__ == "__main__":
    main()
