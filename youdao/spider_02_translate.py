import hashlib

import js2py
import requests

js_info = """
    var r = "" + (new Date).getTime()
    var i = r + parseInt(10 * Math.random(), 10)
    """
context = js2py.EvalJs()
context.execute(js_info)

keyword = input("输入: ")
sign = hashlib.md5()
sign_text = "fanyideskweb" + keyword + context.i + "p09@Bn{h02_BIEe]$P^nG"
sign.update(sign_text.encode())

bv = hashlib.md5()
bv_text = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
bv.update(bv_text.encode())

data = {
    "i": keyword,
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": context.i,
    "sign": sign.hexdigest(),
    "ts": context.r,
    "bv": bv.hexdigest(),
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_REALTIME",
    "typoResult": "false"
}

url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Referer": "http://fanyi.youdao.com",
    # "Cookie": "OUTFOX_SEARCH_USER_ID=-1969069347@10.168.8.64; JSESSIONID=aaa5xcpzvuKmXduHbDYEw; OUTFOX_SEARCH_USER_ID_NCOO=1456165369.47287; ___rl__test__cookies=1544887243270"
    # 用户登录后的cookie
    "Cookie": "OUTFOX_SEARCH_USER_ID=-1969069347@10.168.8.64; JSESSIONID=aaa5xcpzvuKmXduHbDYEw; OUTFOX_SEARCH_USER_ID_NCOO=1456165369.47287; DICT_SESS=v2|E6QEXtOjVY56MkWOfYM0wyhLJuOfk506unMgLnfquRgz0LzEPLzMRzWk4gyOfpy0OGPLgKhHzW0zY64lWRfzf0UG6LUWkfeB0; DICT_PERS=v2|urstoken||DICT||web||-1||1544887617271||122.225.58.147||small_spider_p@163.com||T4kLpFOMUA0kERLkG64Jz0zEn4YGOMgFRp40Lpz0Mkf0gL6Lp4O464ReZOMeLOflWRqLPLeynMgL0lM0HkA0LqB0; DICT_LOGIN=3||1544887617278; ___rl__test__cookies=1544887624241"
}

response = requests.post(url=url, headers=headers, data=data).json()
print(response["translateResult"][0][0]["tgt"])


# 1. 完全还原请求
# 2. 修改部分参数
#    通过参数的不同分析请i去参数发生变化(定位我们最终目的)
# 3. 开始js逆向追踪, 输入请求,寻找断点调式
# 4.