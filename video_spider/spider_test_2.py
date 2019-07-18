"""
抓取网站视屏链接
"""
import urllib
from urllib.parse import urlencode
from urllib.request import Request


def get_html():
    url = "http://www.auto-mooc.com/api/v3/class/gettask"

    info = {
        "class_id": "EC209CF2D6F8EEFD06FCE3CFE8C20AEB",
        "major_id": "SQ180902A",
        "is_user": "0"
    }

    data = urlencode(info).encode()

    request = Request(url=url, data=data)
    response = urllib.request.urlopen(request)
    html = response.read().decode()
    return html


