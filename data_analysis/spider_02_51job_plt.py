import re
from urllib.parse import quote

import requests
from lxml import etree
from queue import Queue
from matplotlib import pylab as plt


class JobPlt():
    def __init__(self):
        self.plt_1 = []
        self.plt_2 = []
        self.plt_3 = []
        self.plt_4 = []
        self.plt_5 = []
        self.url_list = []
        self.html_list = Queue()
        self.key = input("工作名:")
        self.base_url = "https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.html?"

    def get_url_list(self):
        return [self.base_url.format(quote(quote(self.key)), page) for page in range(1, 20)]

    def get_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            self.html_list.put(response.text)
        return None

    def get_item(self):
        html = self.html_list.get()
        x_html = etree.HTML(html)
        money_list = x_html.xpath('//div[@class="el"]/span[3]/text()')[1:]
        for money in money_list:
            money_int = re.match(r'((.*)-(.*))万/月', money)
            if money_int:
                num_1 = float(money_int.group(2))
                if 0.5 <= num_1 <= 1:
                    self.plt_1.append(num_1)
                elif 1 <= num_1 <= 1.5:
                    self.plt_2.append(num_1)
                elif 1.5 <= num_1 <= 2:
                    self.plt_3.append(num_1)
                elif 2 <= num_1 <= 3:
                    self.plt_4.append(num_1)
                elif 3 <= num_1:
                    self.plt_5.append(num_1)
        self.html_list.task_done()

    def save_plt(self):
        x = [len(self.plt_1), len(self.plt_2), len(self.plt_3), len(self.plt_4)]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.pie(x,
                labels=['5-10月薪', '10-15K', '15-20K', '20K-30K'],
                labeldistance=1.2,  # 设置标签距离圆心的距离（0为 圆饼中心数 1为圆饼边缘）
                autopct="%1.1f%%",  # 1.1f% 保留一位小数的百分比
                pctdistance=0.5,  # 比例值文字距离圆心的距离
                explode=[0, 0.2, 0, 0],  # 每一块顶点距圆形的长度
                colors=["red", "blue", "yellow", "green"],  # 最好一一对应
                shadow=True,  # 是否有阴影
                startangle=60,  # 第一块开始的角度
                )
        plt.axis('equal')  # 该行代码使饼图长宽相等
        # plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
        # plt.loc =  'upper right'    # 位于右上角
        # plt.bbox_to_anchor=[0.5, 0.5]   # 外边距 上边 右边
        # plt.ncol=2  # 分两列
        # plt.borderaxespad = 0.3 # 图例的内边距
        # plt.title("上海市{}岗位薪资占比".format(self.key))
        plt.savefig('饼图参数')
        plt.show()

    def run(self):
        # 先利用爬虫抓取一定数量的数据(薪资)
        # 尝试插入数据库
        # 再把数据传递给plt绘图
        url_list = self.get_url_list()
        for url in url_list:
            self.get_html(url)  # 获取HTML
            self.get_item()  # 获取数据
        self.save_plt()  # 绘图


job = JobPlt()
job.run()
