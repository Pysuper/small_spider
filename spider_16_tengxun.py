import time
from selenium import webdriver  # 浏览器驱动对象
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 在不需要使用Chrome无界面的时候， 直接注释这两行就可以了
# options.add_argument('--headless')  # 开启无界面模式
# options.add_argument('--disable-gpu')  # 禁用gpu, 解决一些莫名的问题


class Tencent():
    def __init__(self):
        self.browser = webdriver.Chrome("./chromedriver")
        self.wait = WebDriverWait(self.browser, 10)
        # self.options = webdriver.ChromeOptions()  # 创建配置对象
        # # 设置User-Agent
        # self.options.add_argument(
        #     '--user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36')
        #
        # self.options.add_argument('--proxy-server=115.53.32.100:9999')
        self.base_url = "https://careers.tencent.com/search.html?index={}"

    def get_url_list(self):
        return [self.base_url.format(page) for page in range(1, 10)]

    def get_item(self, url):
        self.browser.get(url)
        # recruit_list = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"recruit-title")))   # 设置显示等待，判断当前clss_name的标签是否加载出来
        info_list = self.browser.find_elements_by_xpath('//div[@class="recruit-list"]/a')
        for info in info_list:
            # 这里不能直接使用xpath语法， 元素的内容需要使用.text
            name = info.find_element_by_xpath('./h4').text
            tag = info.find_element_by_xpath('./p[1]/span[1]').text
            place = info.find_element_by_xpath('./p[1]/span[2]').text
            direction = info.find_element_by_xpath('./p[1]/span[3]').text
            date = info.find_element_by_xpath('./p[1]/span[4]').text

            item = {
                "岗位名称": name,
                "标签": tag,
                "工作地点": place,
                "就业方向": direction,
                "发布日期": date
            }
            yield item
        self.browser.close()
        self.browser.quit()

    def parse_item(self, item):
        print(item)

    def run(self):
        for url in self.get_url_list():
            for item in self.get_item(url):
                self.parse_item(item)
            break


work = Tencent()
work.run()
