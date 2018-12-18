#coding:utf-8

from selenium import webdriver

# browser = webdriver.Chrome('/Users/hulk/software/chrome/chromedriver')

# browser = webdriver.PhantomJS('/Users/hulk/software/phantomjs-2.1.1/bin/phantomjs')
# browser.get('https://www.baidu.com')
# print(browser.current_url)

# from bs4 import BeautifulSoup
# soup = BeautifulSoup('<p>Hello</p>', 'lxml')
# print(soup.p.string)

# import tesserocr

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
	])

if __name__=="__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()






