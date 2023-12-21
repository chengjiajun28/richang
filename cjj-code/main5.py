import requests

cookies = {
    'SUNWAY-ESCM-COOKIE': '9770e778-fa1c-4fae-9fab-9f7c77814ba4',
    '__jsluid_s': '7b79ff19e788059184debcf08dac7874',
    'JSESSIONID': '89379D9DD0694958BA8AADCBCD9CC0E0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    # 'Cookie': 'SUNWAY-ESCM-COOKIE=9770e778-fa1c-4fae-9fab-9f7c77814ba4; __jsluid_s=7b79ff19e788059184debcf08dac7874; JSESSIONID=89379D9DD0694958BA8AADCBCD9CC0E0',
    'Origin': 'https://ec.minmetals.com.cn',
    'Referer': 'https://ec.minmetals.com.cn/logonAction.do',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.post('https://ec.minmetals.com.cn/open/homepage/public', cookies=cookies, headers=headers)

print(response.text)