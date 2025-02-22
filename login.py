import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }


def login():
    print("================登录================")
    url_01 = 'https://wenshu.court.gov.cn/tongyiLogin/authorize'
    resp_01 = requests.post(url=url_01, data={}, headers=headers)
    # print(resp_01.cookies.items())

    url_02 = resp_01.text

    resp_02 = requests.get(url=url_02, headers=headers, allow_redirects=False)
    print(resp_02)

    url_03 = 'https://account.court.gov.cn/captcha/getBase64'
    cookie_03 = {
        resp_02.cookies.items()[0][0]: resp_02.cookies.items()[0][1],
    }
    resp_03 = requests.get(url_03, headers=headers, cookies=cookie_03)
    data_03 = resp_03.json()
    print(data_03['data']['sessionId'])

    url_04 = 'https://account.court.gov.cn/api/securityProtectionSwitch'
    cookie_04 = {
        resp_02.cookies.items()[0][0]: resp_02.cookies.items()[0][1],
    }
    resp_04 = requests.get(url=url_04, headers=headers, cookies=cookie_04)
    # print(resp_04.json())

    post_data = {
        'username': '159********',  # 账号
        # 需要去拦截post请求查看，没时间去查看加密过程。但是加密后的密码是可以重复使用的，与使用明文密码没有太大差别
        'password': 'ZXJcdMH18JMFtwWsomPVLdBOHwWLrqUbrxi%2FPL%2B8LNDr0b7s2oXJoPPW0ZLqsCM4p61%2Bs6if3KJa6pHoCVuFmmWjQz82u5kukA0LWguslFOYW1a%2FvH56EwZlXqRZuGk3ZrhsdK5cWka6SjLJDR%2FPlR877YU6DJpQEvzGP9o0vEIxWcck6gPoi3SpewcF5abm183ZJaC1sQi0wrFXfH2PFdNktqzStl%2B9CwXphnTx34BxGH7Q%2BU6iVmfKBAvMS9QPyyX%2Fl8ya9JlsW9nUABwbNEEu7pdbeL0TgtmNYaGI3CRIqiniLicLr0XZ6n2cHRwU3NFvGhYdvYbyY7KBJHXHxw%3D%3D',
        'appDomain': 'wenshu.court.gov.cn',
    }

    url_05 = 'https://account.court.gov.cn/api/login'
    cookie_05 = {
        resp_02.cookies.items()[0][0]: resp_02.cookies.items()[0][1],
    }
    resp_05 = requests.post(url=url_05, data=post_data, cookies=cookie_05)
    # print(resp_05.json())

    url_06 = resp_01.text
    cookie_06 = {
        resp_05.cookies.items()[0][0]: resp_05.cookies.items()[0][1]
    }
    resp_06 = requests.get(url=url_06, headers=headers, cookies=cookie_06, allow_redirects=False)
    # print(resp_06)

    url_07 = resp_06.headers['Location']
    cookie_07 = {
        resp_01.cookies.items()[0][0]: resp_01.cookies.items()[0][1],
    }
    resp_07 = requests.get(url=url_07, headers=headers, cookies=cookie_07)
    # print(resp_07)
    print(resp_01.cookies.items())
    print("================登录完成================")
    return resp_01.cookies.items()

#
# if __name__ == '__main__':
#     session = login()
#     print(session)  # 获取到的sessionId即可登录



