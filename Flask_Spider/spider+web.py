import json
import os

import requests
import flask as flask
from pprint import pprint

from flask import render_template


class Epidemic(object):
    """获取最新疫情数据"""

    def __init__(self):
        self.cities = []
        self.url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'

    def get_html(self, url):
        """
        获取网页中的数据
        :param url: 网页URL
        :return: 当前网页源码
        """
        response = requests.get(url, timeout=500)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def parse_html(self, html):
        """
        返回JSON数据类型的data数据
        :param html: 当前网页源码
        :return: 网页中的JSON数据信息
        """
        if html == None:
            return None
        data = json.loads(html)["data"]
        return json.loads(data)

    def parse_data(self, data):
        """
        将网页中的数据，存储到Dict中
        :param data: JSON格式的网页数据
        :return: 将数据保存到全局变量 self.cities 中
        """
        date = data['lastUpdateTime']
        china = data['areaTree'][0]['children']  # 国家
        for province in china:  # 省
            province_list = province['children']

            for city in province_list:  # 市
                city_dict = {
                    'date': date,
                    'province_name': province['name'],
                    'city_name': city['name'],
                    'today_confirm': city['today']['confirm'],
                    'total_confirm': city['total']['confirm'],
                    'total_heal': city['total']['heal'],
                    'total_dead': city['total']['dead']
                }
                try:
                    city_dict['today_heal'] = city['today']['heal']
                    city_dict['today_dead'] = city['today']['dead']
                except:
                    city_dict['today_heal'] = 0
                    city_dict['today_dead'] = 0
                self.cities.append(city_dict)

    def save_to_file(self, item):
        """
        将获取到的数据保存到文件中
        :param item: Dict组成的List数据
        :return: 数据保存状态
        """
        pass

    def save_to_sql(self, item):
        """
        将获取到的数据保存到SQL中：MySQL、Redis、MongoDB...
        :param item: Dict组成的List数据
        :return: 数据保存到数据中的保存状态
        """
        pass

    def run(self):
        html = self.get_html(self.url)
        data = self.parse_html(html)
        self.parse_data(data)
        return self.cities


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(BASE_DIR, 'templates')
static = os.path.join(BASE_DIR, 'static')
server = flask.Flask(__name__, template_folder=templates, static_folder=static)  # 创建一个flask对象


@server.route('/', methods=["GET"])
def items():
    data = Epidemic().run()
    # return json.dumps({"code": 0, "msg": "", "count": 100000, "data": data})
    return render_template('LayUI.html', data=data)


server.run(port=8090, debug=True)
