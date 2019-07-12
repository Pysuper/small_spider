import time

from selenium import webdriver


class Taobao():
    """淘宝的数据需要登陆后才能获取"""

    def __init__(self):
        self.base_url = "https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fspm%3Da21bo.2017.754894437.3.5af911d96dD87y%26ad_id%3D%26am_id%3D%26cm_id%3D%26pm_id%3D1501036000a02c5c3739"
        self.browser = webdriver.Chrome("./chromedriver")

    def selenium_parse(self):
        self.browser.get(self.base_url)  # 打开页面

        # 用户登录
        self.browser.find_element_by_xpath('//i[@class="iconfont static"]').click()
        self.browser.find_element_by_id('TPL_username_1').send_keys("824回忆这首歌")
        self.browser.find_element_by_xpath('//input[@class="login-text"]').send_keys("ZXT,960417")
        # 拖动滑块移动
        self.browser.find_element_by_xpath('//span[@class="nc-lang-cnt"]')
        self.browser.find_element_by_xpath('//button[@class="J_Submit"]').click()

        time.sleep(1)

        # 输入数值检索
        self.browser.find_element_by_xpath('//div[@class="search-combobox-input-wrap"]/input').send_keys("MacBookPro")
        self.browser.find_element_by_xpath('//button[@class="btn-search tb-bg"]').click()

        time.sleep(1)
        self.browser.close()

    def run(self):
        self.selenium_parse()


taobao = Taobao()
taobao.run()
