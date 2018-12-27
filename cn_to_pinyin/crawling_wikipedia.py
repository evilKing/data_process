# coding=UTF-8
import requests
from scrapy import Selector
import requests.adapters
import time
import urllib.parse
import math
import json
import threading
import re
from os.path import join as join_path, abspath, dirname
import time
import traceback
import argparse
import urllib.parse
import requests
from pymongo import MongoClient
from gevent.pool import Pool
import gevent
from redis import StrictRedis, ConnectionPool

model_path = join_path(abspath(dirname(__file__)), '')
args_parser = argparse.ArgumentParser()
args_parser.add_argument('--pool_num', type=int, default=0)
cmdl_args = args_parser.parse_args()
redis_queue = StrictRedis(connection_pool=ConnectionPool(host='127.0.0.1', port=6379, db=4, decode_responses=True))
COMP_LINK = "comp_link"  # *
COMP_HTML = "comp_html"  # *
DECADE_LINK = "decade_link"
DECADE_HTML = "decade_html"


# -------------------------------------------

class Crawling:
	def __init__(self):

		self.value = set()
		self.base_url = "https://zh.wikipedia.org{0}"
		self.base_url = "https://en.wikipedia.org{0}"
		self.client = MongoClient()["crawling"]["wikipedia_en"]
		self.client.ensure_index('company_link', unique=True)
		self.proxy = {
			"http:": "127.0.0.1:1087",
			"https": "127.0.0.1:1087"
		}
		self.list_links = set()
		self.comp_links = set()

	def get_html(self, url, d=100):

		n = 0
		h = ""
		if "//zh.wikipedia.org" in url:
			url = url.replace("/wiki/", "/zh-cn/")
		while not h and n < d:
			n += 1
			try:
				h = requests.get(url, proxies=self.proxy, timeout=5).text
			# html.encoding="utf-8"
			# print(html.text)
			except Exception as e:
				h = ""
			if "Wikimedia Error" in h:
				h = ""
			time.sleep(5)

		if not h:
			print(url)
		return h

	def get_comp_html(self, h):
		selector = Selector(text=h)
		url = "".join(selector.xpath("""//link[@rel="canonical"]/@href""").extract())
		if self.client.find_one({"company_link": url}):
			return
		info = []

		table_xpath = """//table[@class="infobox vcard"]"""
		name = selector.xpath(table_xpath+"/caption/text()").extract()
		table_nums = len(selector.xpath(table_xpath))

		for tn in range(1, table_nums + 1):
			info_xpath = table_xpath + "[" + str(tn) + """]/tbody/tr"""
			info_nums = len(selector.xpath(info_xpath))
			for inn in range(1, info_nums + 1):
				info_th = selector.xpath(info_xpath + "[" + str(inn) + """]/th""").xpath("string(.)").extract()
				info_td = selector.xpath(info_xpath + "[" + str(inn) + """]/td""").xpath("string(.)").extract()
				info.append(["|".join(info_th), "|".join(info_td)])
		profile = selector.xpath("""//div[@class="mw-parser-output"]/p[1]""").xpath("string(.)").extract()
		keys = selector.xpath("""//div[@class="mw-parser-output"]/p[1]/b""").xpath("string(.)").extract()
		result = {
			"name":name,
			"info": info,
			"profile": profile,
			"keys": keys,
			"company_link": url
		}
		self.client.insert_one(result)

	def get_decade_link(self, h):
		selector = Selector(text=h)
		links = set(selector.xpath("""//div[@id="mw-pages"]//a/@href""").extract()) | \
				set(selector.xpath("""//div[@id="mw-subcategories"]//a/@href""").extract())
		url = "".join(selector.xpath("""//link[@rel="canonical"]/@href""").extract())
		if "https://en.wikipedia" in url:
			base_url = "https://en.wikipedia.org{0}"
		else:
			base_url = "https://zh.wikipedia.org{0}"
		category_link = set(filter(lambda x: "Category" in x, links))
		comp_links = links - category_link
		for k in category_link:
			if k not in self.list_links:
				redis_queue.rpush(DECADE_LINK, base_url.format(k))
			self.list_links.add(k)

		for k in comp_links:
			if k not in self.comp_links:
				redis_queue.rpush(COMP_LINK, base_url.format(k))
			self.comp_links.add(k)


def push_key():
	"""生产"""
	# keys = [
	# 	# "https://en.wikipedia.org/w/index.php?title=Category:Companies_by_year_by_country&subcatfrom=1969%0ACompanies+established+in+1969+by+country#mw-subcategories",
	# 	# 	"https://en.wikipedia.org/wiki/Category:Companies_by_year_by_country",
	# 	"https://en.wikipedia.org/wiki/Category:Companies_by_year_of_establishment"]
	keys = []
	for k in keys:
		# k_html = crawling.get_html(k)
		# crawling.get_decade_link(k_html)
		redis_queue.rpush(DECADE_LINK, k)
	print(len(keys))


def run_decade():
	"""调度"""
	while True:
		cos_id = redis_queue.lpop(DECADE_LINK)
		if cos_id:
			try:
				html = crawling.get_html(cos_id)
				redis_queue.rpush(DECADE_HTML, html)
			except Exception as e:
				gevent.sleep(50)
		else:
			if not redis_queue.llen(DECADE_HTML) and not redis_queue.llen(DECADE_LINK):
				gevent.sleep(50)
				if not redis_queue.llen(DECADE_LINK) and redis_queue.llen(COMP_LINK) \
						and not redis_queue.llen(DECADE_HTML):
					print("decade link queue is empty")

					break
			else:
				gevent.sleep(5)


def parse_decade():
	while True:
		cos_id = redis_queue.lpop(DECADE_HTML)
		if cos_id:
			try:
				crawling.get_decade_link(cos_id)
			except Exception as e:
				traceback.print_exc()
		else:
			time.sleep(10)
			if not redis_queue.llen(DECADE_LINK) and not redis_queue.llen(DECADE_HTML):
				gevent.sleep(60)
				if not redis_queue.llen(DECADE_HTML) and redis_queue.llen(COMP_LINK) \
					and not redis_queue.llen(DECADE_LINK):
					print("decade html queue is empty")
					break
			else:
				gevent.sleep(5)




def run_comp():
	"""调度"""
	while True:
		cos_id = redis_queue.lpop(COMP_LINK)
		if cos_id:
			try:
				if crawling.client.find_one({"company_link": cos_id}):
					continue
				html = crawling.get_html(cos_id)
				redis_queue.rpush(COMP_HTML, html)
			except Exception as e:
				traceback.print_exc()
		else:
			if not redis_queue.llen(DECADE_LINK) and not redis_queue.llen(DECADE_HTML):
				gevent.sleep(230)
				if not redis_queue.llen(COMP_LINK) and not redis_queue.llen(DECADE_LINK) and not redis_queue.llen(DECADE_HTML):
					print("company link queue is empty")
					break
			else:
				gevent.sleep(5)


def parse_comp():
	while True:
		cos_id = redis_queue.lpop(COMP_HTML)
		if cos_id:
			try:
				crawling.get_comp_html(cos_id)
			except Exception as e:
				traceback.print_exc()
		else:
			if not redis_queue.llen(DECADE_LINK) and not redis_queue.llen(DECADE_HTML) \
				and not redis_queue.llen(COMP_LINK):
				gevent.sleep(240)
				if not redis_queue.llen(COMP_HTML) and not redis_queue.llen(DECADE_LINK) and not redis_queue.llen(DECADE_HTML):
					print("company html queue is empty")

					break
			else:
				gevent.sleep(5)



def gevent_for_decade(rd=5, pd=2, rc=8, pc=2):
	import gevent.monkey
	gevent.monkey.patch_all()
	push_key()
	p = Pool(rd + pd + rc + pc)
	for i in range(rd):
		p.apply_async(run_decade)
	for i in range(pd):
		p.apply_async(parse_decade)
	for i in range(rc):
		p.apply_async(run_comp)
	for i in range(pc):
		p.apply_async(parse_comp)
	p.join()


crawling = Crawling()
if __name__ == '__main__':
	# parse_brand()
	# gevent_for_html(rd=10, pd=2, rr=15, pr=3, rc=25, pc=5)
	gevent_for_decade(rd=15, pd=2, rc=15, pc=3)

	# s = time.time()
	# get_data_with_for()
	# print(time.time() - s)
	#
	# test_html = crawling.get_html("https://en.wikipedia.org/wiki/WorldQuant")
	# print(crawling.get_comp_html(test_html))
