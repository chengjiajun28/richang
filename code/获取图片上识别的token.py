import requests

import json


def main():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=wc6Gc1Ckzz0v3Ylo2dz7BMMc&client_secret=oQfZtGnrbUgNK48fnUyoyMRp5swhVvbE"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()