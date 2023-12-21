# encoding:utf-8

import base64
import os
import re

import requests


def orc_request(path):
    '''
    通用文字识别（高精度版）
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '24.fdc1a72218bd3828b8a627738740deac.2592000.1704960395.282335-38507260'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print(response.json())

        return response.json()['words_result'][0]["words"]


def process_expression(expression):
    global result
    pattern = r"(\d+)([+\-*\/x])(\?=)(\d+)"
    matches = re.search(pattern, expression)

    if matches:
        num1 = int(matches.group(1))
        operator = matches.group(2)
        num2 = int(matches.group(4))
        try:
            num3 = int(matches.group(5))

            num2 = int(str(num2) + str(num3))
        except Exception as e:
            pass

        if operator == '+':
            result = num2 - num1
        elif operator == '-':
            result = num2 + num1
        elif operator == 'x':
            result = num2 // num1
        elif operator == '/':
            result = num2 * num1

        return result

    return "Invalid expression"


def remove_path(path):
    try:
        os.remove(path)
        print(f"文件 {path} 已成功删除。")
    except OSError as e:
        print(f"删除文件时出错: {e}")
