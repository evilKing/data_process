#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# browser = webdriver.Chrome()
# try:
# 	browser.get('https://www.baidu.com')
# 	input = browser.find_element_by_id('kw')
# 	input.send_keys('Python')
# 	input.send_keys(Keys.ENTER)
#
# 	wait = WebDriverWait(browser, 10)
# 	wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
# 	print(browser.current_url)
# 	print(browser.get_cookies())
# 	print(browser.page_source)
# finally:
# 	browser.close()

# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input_first = browser.find_element_by_id('q')
# input_second = browser.find_element_by_css_selector('#q')
# input_third = browser.find_element_by_xpath('//*[@id="q"]')
# print(input_first, input_second, input_third)
# browser.close()

# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# lis = browser.find_elements_by_css_selector('.service-bd li')
# print(lis)
# browser.close()

import time

# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input = browser.find_element_by_id('q')
# input.send_keys('iPhone')
# time.sleep(1)
# input.clear()
# input.send_keys('iPad')
# button = browser.find_element_by_class_name('btn-search')
# button.click()


from selenium.webdriver import ActionChains

# browser = webdriver.Chrome()
# url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)
# browser.switch_to.frame('iframeResult')
# source = browser.find_element_by_css_selector('#draggable')
# target = browser.find_element_by_css_selector('#droppable')
# actions = ActionChains(browser)
# actions.drag_and_drop(source, target)
# actions.perform()


# browser = webdriver.Chrome()
# browser.get('https://www.zhihu.com/explore')
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom")')

# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# logo = browser.find_element_by_id('zh-top-link-logo')
# print(logo)
# print(logo.get_attribute('class'))
#
# input = browser.find_element_by_class_name('zu-top-add-question')
# print(input.text)

# input = browser.find_element_by_class_name('zu-top-add-question')
# print(input.id)
# print(input.location)
# print(input.tag_name)
# print(input.size)


# browser = webdriver.Chrome()
# browser.get('https://www.baidu.com/')
# browser.get('https://www.taobao.com/')
# browser.get('https://www.python.org/')
# browser.back()
# time.sleep(1)
# browser.forward()
# browser.close()


# browser = webdriver.Chrome()
# browser.get('https://www.zhihu.com/explore')
# print(browser.get_cookies())
# browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})
# print(browser.get_cookies())
# browser.delete_all_cookies()
# print(browser.get_cookies())


# browser = webdriver.Chrome()
# browser.get('https://www.baidu.com')
# browser.execute_script('window.open()')
# print(browser.window_handles)
# browser.switch_to_window(browser.window_handles[1])
# browser.get('https://www.taobao.com')
# time.sleep(1)
# # browser.switch_to_window(browser.window_handles[0])
# browser.switch_to.window(browser.window_handles[0])
# browser.get('https://python.org')


from selenium.common.exceptions import TimeoutException, NoSuchElementException

# browser = webdriver.Chrome()
# try:
# 	browser.get('https://www.baidu.com')
# except TimeoutException:
# 	print('Time Out')
#
# try:
# 	browser.find_element_by_id('hello')
# except NoSuchElementException:
# 	print('No Element')
# finally:
# 	browser.close()

# 使用 Headless 模式
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.get('htts://www.baidu.com')


SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.get('htts://www.baidu.com')