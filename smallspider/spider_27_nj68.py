# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : Zheng Xingtao
# File      : spider_27_nj68.py
# Datetime  : 2020/5/15 上午9:31
import time

from selenium import webdriver  # 导入库
from selenium.webdriver import ActionChains

browser = webdriver.Chrome("./chromedriver")  # 声明浏览器-->指明driver路径
# url = "https://item.taobao.com/item.htm?spm=a230r.1.14.23.76c71ea52MoYIU&id=611354061932&ns=1&abbucket=13#detail"
# browser.get(url)  # 打开浏览器预设网址
#
# browser.switch_to.frame("sufei-dialog-content") # iframe
# browser.find_element_by_id('fm-login-id').send_keys("824回忆这首歌")
# time.sleep(1)
# browser.find_element_by_id('fm-login-password').send_keys("ZXT,960417")
# time.sleep(1)
# sour = browser.find_element_by_id("nc_1_n1z")
# ele = browser.find_element_by_class_name("nc-lang-cnt")
# ActionChains(browser).drag_and_drop_by_offset(sour, ele.size['width'], sour.size['height']).perform()   # 鼠标滑动
# time.sleep(2)
# browser.find_element_by_xpath('//div[@class="fm-btn"]/button').click()
# print(browser.page_source)  # 打印网页源代码
# browser.close()  # 关闭浏览器


url = "https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=nj68+%E9%94%AE%E7%9B%98&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
browser.get(url)

# 用户登录
# browser.switch_to.frame("sufei-dialog-content") # iframe
browser.find_element_by_id('fm-login-id').send_keys("824回忆这首歌")
time.sleep(1)
browser.find_element_by_id('fm-login-password').send_keys("ZXT,960417")

sour = browser.find_element_by_xpath('//span[@id="nc_1_n1z"]')
ele = browser.find_element_by_id("nc_1__scale_text")

print(sour, ele.size['width'], sour.size['height'])

ActionChains(browser).drag_and_drop_by_offset(sour, ele.size['width'], sour.size['height']).perform()   # 鼠标滑动
time.sleep(2)
browser.find_element_by_xpath('//div[@class="fm-btn"]/button').click()
