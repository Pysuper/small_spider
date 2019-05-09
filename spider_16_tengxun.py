import requests
url = "https://careers.tencent.com/search.html?index=2"
header = {
    "cookie": "_ga=GA1.2.1909285086.1554912381; pgv_pvi=3052375040; _gcl_au=1.1.1365864570.1554912382",
    "referer": "https://careers.tencent.com/citymain.html",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "upgrade-insecure-requests": 1
}

def get_html(url):
    response = requests.get(url, header)
    response.encoding = response.apparent_encoding
    return response.text

html = get_html(url)
print(html)