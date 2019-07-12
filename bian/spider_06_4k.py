import urllib
from urllib.request import Request
import requests
from lxml import etree


class FourK():
    def __init__(self):
        self.base_url = "http://pic.netbian.com/4kmeinv/index_{}.html"
        self.header = {
            "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Cookie": "__cfduid=de1ca3d0fc5b6a90b5d903b52412785321562603023; PHPSESSID=9cc88ab3ab1aa3d113beb9f54148a579; zkhanmlusername=%D3%F6%BC%FB%C0%EE%D0%A1%CD%C3; zkhanmluserid=1558778; zkhanmlgroupid=1; zkhanmlrnd=VOUC33tiHcjMKLUZEQ0n; zkhanmlauth=c22c7e6b41727e6379d8346f0eedb5bb; yjs_id=cb1ae96ac5806c14eb8d6460ccd29ade; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1562603029; ctrl_time=2; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562603172; security_session_verify=e35e1a2cc1bbc63e145571dc88981222; zkhandownid24424=2",
        }

    def get_url_list(self):
        url_list = []
        for page in range(1, 10):
            if page == 1:
                url_list.append("http://pic.netbian.com/4kmeinv/index.html")
            else:
                url_list.append(self.base_url.format(page))
        return url_list

    def get_html(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            return response.text
        return None

    def parse_html(self, html):
        xpath_html = etree.HTML(html)
        src_list = xpath_html.xpath('//ul[@class="clearfix"]/li/a/@href')
        for src in src_list:
            yield src

    def parse_detail_html(self, detail_url):
        print(detail_url)

    def save_item(self, item):
        pass

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            for detail_url in self.parse_html(html):
                self.parse_detail_html("http://pic.netbian.com" + detail_url)
            break


image = FourK()


# image.run()


# a = "zkhanmlusername=%D2%BB%C6%DF%C4%EA%CA%AE%D4%C2%CB%C4%BA%C5; zkhanmluserid=1325919; zkhanmlgroupid=1; zkhanmlrnd=ryxqsnasMerQx6LjPcYH; zkhanmlauth=d7e148379489eda99ba46f16ca17ca30; yjs_id=3746932221559f4c9cb62c64ec8d5fe1; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1562600967; ctrl_time=2; security_session_verify=ff59f24c8cff3709340180dcf3d4947f; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562600992"
# info = {"msg": 4, "pic": "/downpic.php?id=24424&classid=66"}
# inf2o = {"msg": 4, "pic": "/downpic.php?id=17781&classid=54"}

def de_1():
    header = {
        "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Cookie": "__cfduid=de1ca3d0fc5b6a90b5d903b52412785321562603023; "
                  "PHPSESSID=9cc88ab3ab1aa3d113beb9f54148a579; "
                  "zkhanmlusername=%D3%F6%BC%FB%C0%EE%D0%A1%CD%C3; "
                  "zkhanmluserid=1558778; "
                  "zkhanmlgroupid=1; "
                  "zkhanmlrnd=VOUC33tiHcjMKLUZEQ0n; "
                  "zkhanmlauth=c22c7e6b41727e6379d8346f0eedb5bb; "
                  "yjs_id=cb1ae96ac5806c14eb8d6460ccd29ade; "
                  "Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1562603029; "
                  "ctrl_time=2; "
        # "Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562603172; "
                  "Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562603781; "
        # "security_session_verify=e35e1a2cc1bbc63e145571dc88981222; "
                  "security_session_verify=4fcbd3cd3b13d3f5d7efc35e22cdc1be; "
                  "zkhandownid17781=2",
    }

    # req = urllib.request.Request(url="http://pic.netbian.com/downpic.php?id=24424&classid=66", headers=header)
    req = urllib.request.Request(url="http://pic.netbian.com/downpic.php?id=17781&classid=54", headers=header)
    content = urllib.request.urlopen(req).read()

    with open("./image/asds.jpg", 'wb') as f:
        f.write(content)
        print("下载完成...")


def de_2():
    header = {
        "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        # "Cookie": "__cfduid=de1ca3d0fc5b6a90b5d903b52412785321562603023; "
        #           "PHPSESSID=9cc88ab3ab1aa3d113beb9f54148a579; "
        #           "zkhanmlusername=%D3%F6%BC%FB%C0%EE%D0%A1%CD%C3; "
        #           "zkhanmluserid=1558778; "
        #           "zkhanmlgroupid=1; "
        #           "zkhanmlrnd=VOUC33tiHcjMKLUZEQ0n; "
        #           "zkhanmlauth=c22c7e6b41727e6379d8346f0eedb5bb; "
        #           "yjs_id=cb1ae96ac5806c14eb8d6460ccd29ade; "
        #           "Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1562603029; "
        #           "ctrl_time=2; "
        #             # "Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562603172; "
        #           "Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562603781; "
        #             # "security_session_verify=e35e1a2cc1bbc63e145571dc88981222; "
        #           "security_session_verify=4fcbd3cd3b13d3f5d7efc35e22cdc1be; "
        #           "zkhandownid17781=2",
        "Cookie": "__cfduid=de1ca3d0fc5b6a90b5d903b52412785321562603023;"
               "PHPSESSID=9cc88ab3ab1aa3d113beb9f54148a579;"
               "zkhanmlusername=%D3%F6%BC%FB%C0%EE%D0%A1%CD%C3;"
               "zkhanmluserid=1558778;"
               "zkhanmlgroupid=1;"
               "zkhanmlrnd=VOUC33tiHcjMKLUZEQ0n;"
               "zkhanmlauth=c22c7e6b41727e6379d8346f0eedb5bb;"
               "yjs_id=cb1ae96ac5806c14eb8d6460ccd29ade;"
               "Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1562603029;"
               "ctrl_time=2;"
               "security_session_verify=227a276bb4f4757637ee0ff3df9015d7;"
               "Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1562604417"
    }
    response = requests.get("http://pic.netbian.com/e/extend/downpic.php?id=24413&t=0.04221579160046196",
                            headers=header)
    print(response.text)


de_2()
