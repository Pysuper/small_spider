import requests

# 首先使用手机端登录账号, 获取cookie
session = requests.session()
response = session.post(
    url="http://account.youdao.com/loginproxy",
    headers={
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "Referer": "http://account.youdao.com/login?service=dict&back_url=http%3A%2F%2Fdict.youdao.com%2Fsearch%3Fq%3Das%26tab%3D%23keyfrom%3D%24%7Bkeyfrom%7D&m=1",
        "Cookie": "OUTFOX_SEARCH_USER_ID=-1839255848@180.155.232.32; _ntes_nnid=4ef604fb9dd8c8fc483a6a12c09eef31,1544494790454; OUTFOX_SEARCH_USER_ID_NCOO=346349777.2633203; YOUDAO_MOBILE_ACCESS_TYPE=0"
    },
    data={
        "type": "1",
        "url": "http://account.youdao.com/login?back_url=http%3A%2F%2Fdict.youdao.com%2Fsearch%3Fq%3Das%26tab%3D%23keyfrom%3D%24%7Bkeyfrom%7D&m=1&service=dict&success=1",
        "product": "search",
        "url2": "http://account.youdao.com/login?back_url=http%3A%2F%2Fdict.youdao.com%2Fsearch%3Fq%3Das%26tab%3D%23keyfrom%3D%24%7Bkeyfrom%7D&m=1&service=dict&error=1",
        "username": "small_spider_p@163.com",
        "password": "zxt@yj0407",
        "savelogin": "1",
        "submit": " 登 录 "
    }
)

# 手机端无法登陆?

cookie = response.cookies
print(response.cookies)
print(requests.utils.dict_from_cookiejar(cookie))

# with open("./youdao.html", "wb") as f:
#     f.write(response.content)
