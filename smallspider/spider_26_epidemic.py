import json
import requests


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
                    '日期': date,
                    '省份': province['name'],
                    '市': city['name'],
                    '新增确认': city['today']['confirm'],
                    '累计确认': city['total']['confirm'],
                    '累计治愈': city['total']['heal'],
                    '累计死亡': city['total']['dead']
                }
                try:
                    city_dict['新增治愈'] = city['today']['heal']
                    city_dict['新增死亡'] = city['today']['dead']
                except:
                    city_dict['新增治愈'] = 0
                    city_dict['新增死亡'] = 0
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


Epidemic().run()
