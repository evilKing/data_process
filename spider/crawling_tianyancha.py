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
redis_queue = StrictRedis(connection_pool=ConnectionPool(host='127.0.0.1', port=6379, db=1, decode_responses=True))
COMP_LINK = "comp_link"  # *
COMP_HTML = "comp_html"  # *
REDIS_KEY = "tianyan"
SEARCH_LINK = "search_link"
SEARCH_HTML = "search_html"
BRAND_LINK = "brand_link"
BRAND_HTML = "brand_html"



# -------------------------------------------

class Crawling:
	def __init__(self):
		self.headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
			'Connection': 'keep-alive',
			'Cookie': 'TYCID=27a76f60d2b811e88ae7e3d6e0c34190; undefined=27a76f60d2b811e88ae7e3d6e0c34190; ssuid=4413173240; _ga=GA1.2.1501966850.1539854950; _gid=GA1.2.1498667544.1539854950; RTYCID=90afebb407304b419ffba3f34db2cbbf; CT_TYCID=be7a85298d4b4c5c89c7a318933de9c4; aliyungf_tc=AQAAAGY8MkG+sgsARg5pZTp1l4I4f8ag; csrfToken=fkLdGgQ0KdvwrHEM42ohdewc; cloud_token=a095417bd2c54b658e67f3f5ab221407; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1540014672,1540014676,1540014687,1540024935; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1540024935',
			# 'Host': 'www.tianyancha.com',
			'Referer': 'https://www.baidu.com/link?url=OxKpHBAyow0MbfYxvji6ulLNumykoi-9DJbD724GpNyaSTSCNKNlm4G2pLLHmK1eNbv1X1AkdpfkkdLiuY8tsq&wd=&eqid=f03e551e0004a8c7000000035bcac24c',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		}
		self.value = set()
		self.base_url = "https://www.tianyancha.com/search/p{0}?key={1}"
		self.brand_url = "https://www.tianyancha.com/brand/{0}"
		self.proxy = self.get_ip()
		self.client = MongoClient()["crawling"]["tianyancha"]
		self.client.ensure_index('company_link', unique=True)

		self.brand_client = MongoClient()["crawling"]["tianyancha_brand"]
		self.brand_client.ensure_index('brand_link', unique=True)

	def update_ip(self):
		try:
			self.proxy = self.get_ip()
		except Exception as e:
			print(e)
			time.sleep(300)
			self.update_ip()

	def get_ip(self):
		ip = requests.get("http://10.0.40.42:5000/proxy", headers=self.headers).text
		p = {
			'http': ip,
			'https': ip,
		}

		return p

	def get_html(self, url, d=100):

		n = 0
		h = ""
		while not h and n < d:
			n += 1
			try:
				h = requests.get(url, headers=self.headers, proxies=self.proxy, timeout=1).text
			# html.encoding="utf-8"
			# print(html.text)
			except Exception as e:
				h = ""
				self.update_ip()
			if "无法收到短信验证码？点击切换语音验证" in h:
				h = ""
				self.update_ip()
		return h

	def save(self, fn):
		print(model_path + fn)
		open(model_path + "result/" + fn, "w").write("\n".join(self.value))

	def parse_comp_html(self, h):
		selector = Selector(text=h)
		url = "".join(selector.xpath("""//div[@class="company-tabwarp -abs"]/a/@href""").extract())
		# if not url:
		# 	return
		# if self.client.find_one({"company_link": url}):
		# 	return
		name = selector.xpath("""//div[@class="header"]/h1/text()""").extract()
		update_time = selector.xpath("""//span[@class="updatetimeComBox"]/text()""").extract()
		info_base_xpath = """//div[@class="detail "]/div"""
		info_nums = len(selector.xpath(info_base_xpath).extract())
		info = {}
		for i in range(1, info_nums + 1):
			second_xpath = """//div[@class="detail "]/div""" + str([i]) + """/div"""
			for j in range(1, len(selector.xpath(second_xpath).extract()) + 1):
				info_items = selector.xpath(
					second_xpath + str([j]) + """/span[3]/script/text()""").extract()
				if not (info_items):
					info_items = selector.xpath(second_xpath + str([j]) + """/a/text()""").extract()
				if info_items:
					info_name = selector.xpath(
						second_xpath + str([j]) + """/span[1]/text()""").extract()
					info["".join(info_name)] = "".join(info_items).replace("\"", "")

		common_name = selector.xpath("""//div[@class="logo-text -l4 -w100"]/span/text()""").extract()
		member = []
		member_xpath = """//div[@class="clearfix"]/table/tbody/tr"""
		member_nums = len(selector.xpath(member_xpath).extract())
		for i in range(1, member_nums + 1):
			member_name = selector.xpath(
				member_xpath + str([i]) + """//a[@event-name="企业详情-主要人员"]/text()""").extract()
			member_title = selector.xpath(member_xpath + str([i]) + """/td[3]""").xpath(
				"string(.)").extract()
			member.append(member_name + member_title)

		holder_xpath = """//div[@id="_container_holder"]/table/tbody/tr"""
		holder_nums = len(selector.xpath(holder_xpath).extract())
		holder = []
		for i in range(1, holder_nums + 1):
			holder_name = selector.xpath(
				holder_xpath + str([i]) + """//a[@class="link-click"]/text()""").extract()
			holder_rate = selector.xpath(
				holder_xpath + str([i]) + """//span[@class="num-investment-rate"]/text()""").extract()
			holder_capital = selector.xpath(
				holder_xpath + str([i]) + """/td[4]/div/span/text()""").extract()
			holder_link = selector.xpath(
				holder_xpath + str([i]) + """/td/div/div/a[@class="link-click"]/@href""").extract()
			holder.append(holder_name + holder_rate + holder_capital + holder_link)

		invest_xpath = """//div[@id="_container_invest"]/table/tbody/tr"""
		invest_nums = len(selector.xpath(invest_xpath).extract())
		invest = []
		for i in range(1, invest_nums + 1):
			invest_name = selector.xpath(
				invest_xpath + str([i]) + """/td[2]//a[@class="link-click"]/text()""").extract()
			invest_rate = selector.xpath(
				invest_xpath + str([i]) + """/td[5]/span/text()""").extract()
			invest_representative = selector.xpath(
				invest_xpath + str([i]) + """/td[3]/span[1]/text()""").extract()
			invest_link = selector.xpath(
				invest_xpath + str([i]) + """/td[2]//td/a/@href""").extract()
			invest.append(invest_name + invest_rate + invest_representative + invest_link)

		financing_xpath = """//div[@id="_container_rongzi"]/table/tbody/tr"""
		financing_nums = len(selector.xpath(financing_xpath).extract())
		financing = []
		for i in range(1, financing_nums + 1):
			financing_time = selector.xpath(financing_xpath + str([i]) + """/td[2]/text()""").extract()
			financing_rounds = selector.xpath(financing_xpath + str([i]) + """/td[3]/text()""").extract()
			financing_valuation = selector.xpath(financing_xpath + str([i]) + """/td[4]/text()""").extract()
			financing_investor = selector.xpath(
				financing_xpath + str([i]) + """/td[7]//a/text()""").extract()
			financing_amount = selector.xpath(financing_xpath + str([i]) + """/td[5]/text()""").extract()
			financing.append(financing_time + financing_rounds + financing_valuation + financing_amount + [
				",".join(financing_investor)])

		legal_representative = selector.xpath(
			"""//div[@class="legal-representative"]//div[@class="name"]""").xpath(
			"string(.)").extract()
		tags = selector.xpath("""//span[@class="tag tag-new-category mr10"]/text()""").extract()

		branch_xpath = """//div[@id="_container_branch"]/table/tbody/tr"""
		branch_nums = len(selector.xpath(branch_xpath).extract())
		branch = []
		for i in range(1, branch_nums+1):
			branch_name = selector.xpath(
				branch_xpath + str([i]) + """/td[2]//a[@class="link-click"]/text()""").extract()

			branch_principal = selector.xpath(branch_xpath + str([i]) + """/td[3]""").xpath(
				"string(.)").extract()
			branch_link = selector.xpath(
				branch_xpath + str([i]) + """/td[2]//td/a/@href""").extract()
			branch.append(branch_name + branch_principal + branch_link)

		other_link = selector.xpath(
			"""//div[@class="container-right"]//a[@class="link-hover-click"]/@href""").extract()
		history_name = selector.xpath("""//div[@class="history-content"]/div/text()""").extract()
		en_name = selector.xpath(
			"""//div[@id="_container_baseInfo"]//table[@class="table -striped-col -border-top-none"]/tbody/tr[7]/td[4]/text()""").extract()
		registration_time = selector.xpath(
			"""//div[@id="_container_baseInfo"]//table[@class="table -striped-col -border-top-none"]/tbody/tr[4]/td[2]/span/text()""").extract()
		size = selector.xpath(
			"""//div[@id="_container_baseInfo"]//table[@class="table -striped-col -border-top-none"]/tbody/tr[5]/td[@colspan="2"]/text()""").extract()

		registered_capital = \
			selector.xpath("""//div[@id="_container_baseInfo"]/table[@class="table"]/tbody/tr[1]/td[2]/div[2]/@title""").extract()
		score = "".join(selector.xpath("""//img[@class="sort-chart"]/@alt""").extract()).replace("评分", "")

		team_xpath = """//div[@id="_container_teamMember"]/div/div[@class="card-team"]"""
		team_nums = len(selector.xpath(team_xpath).extract())
		leaders = []
		for tn in range(1, team_nums+1):
			leader_name = selector.xpath(team_xpath+"["+str(tn)+"""]/div[@class="left"]/div/div/img/@alt""").extract()
			leader_position = selector.xpath(team_xpath+"["+str(tn)+"""]/div[@class="right"]/div[@class="title"]/text()""").extract()
			leader_profile = selector.xpath(team_xpath+"["+str(tn)+"""]/div[@class="right"]/p/text()""").extract()
			leaders.append(["".join(leader_name),",".join(leader_position),"\n".join(leader_profile)])
		products_name = selector.xpath("""//div[@class="product-list"]/a/span/text()""").extract()
		products_link = list(map(lambda x: "".join(re.findall("\'([a-z0-9]*)\'", x)),
								 selector.xpath("""//div[@class="product-list"]/a/@onclick""").extract()))

		result = {
			"registration_time": "".join(registration_time),
			"registered_capital":"".join(registered_capital),
			"leaders":leaders,
			"en_name": "".join(en_name),
			"history_name": history_name,
			"common_name": "".join(common_name),
			"other_link": other_link,
			"branch": branch,
			"tags": tags,
			"legal_representative": "".join(legal_representative),
			"holder": holder,
			"company_link": url,
			"invest": invest,
			"member": member,
			"name": "".join(name),
			"update_time": "".join(update_time),
			"financing": financing,
			"info": info,
			"score": score,
			"products": products_name,
			"size":"".join(size)
		}
		# self.client.insert_one(result)
		# brand_link = set(selector.xpath("""//div[@class="item"]/a/@href""").extract())
		# for k in brand_link:
		# 	redis_queue.rpush(BRAND_LINK, k)
		# for k in products_link:
		# 	redis_queue.rpush(BRAND_LINK, self.brand_url.format(k))
		return result

	def parse_link_html(self, h):
		selector = Selector(text=h)
		links = set(selector.xpath("""//div[@class="header"]/a/@href""").extract())
		for k in links:
			redis_queue.rpush(COMP_LINK, k)

		brand_link = set(map(lambda x: self.brand_url.format(x.split("\'")[1]),
							 selector.xpath("""//div[@class="brand"]/@onclick""").extract()))
		for k in brand_link:
			redis_queue.rpush(BRAND_LINK, k)

	def parse_brand_html(self, h):
		selector = Selector(text=h)
		key = re.findall("[a-z0-9]+$", "".join(selector.xpath("""//link[@rel="alternate"]/@href""").extract()))
		url = self.brand_url.format("".join(key))
		if not key:
			return
		if self.brand_client.find_one({"brand_link":url}):
			return
		name = "".join(selector.xpath("""//div[@class="content"]/div[@class="header"]/div/text()""").extract())
		father = "".join(selector.xpath("""//div[@class="content"]/div[@class="header"]/a/text()""").extract())
		tags = selector.xpath("""//div[@class="tags"]/a/text()""").extract()
		info = selector.xpath("""//div[@class="infos"]/span/text()""").extract()
		profile = selector.xpath(
			"""//div[@class="block-data-group"][1]/div[@class="block-data"]/div/text()""").extract()
		leaders_xpath = """//div[@class="block-data-group"][2]/div/div/table/tbody/tr"""
		leaders_nums = len(selector.xpath(leaders_xpath).extract())
		leaders = []
		for n in range(1, leaders_nums + 1):
			person_xpath = leaders_xpath + "[" + str(n) + "]"
			leader_name = "".join(selector.xpath(person_xpath + "/td[2]/table/tr/td[1]/div[2]/img/@alt").extract())
			leader_position = "".join(selector.xpath(person_xpath + "/td[3]/text()").extract())
			leaders.append(leader_name + "\t" + leader_position)
		result = {
			"brand_link": url,
			"name": name,
			"father": father,
			"tags": tags,
			"info": info,
			"profile": "".join(profile),
			"leaders": leaders
		}
		self.brand_client.insert_one(result)


def push_key():
	"""生产"""
	# open(model_path + "data/company_name.txt").read().split("\n")

	# open(model_path + "data/common_name.txt").read().split("\n")

	keys = set(map(lambda x: x.split("\t")[0],open(model_path + "data/bbp_bd_tags.txt").read().split("\n")))
	# ["腾讯", "阿里", "华为", "小米", "呗佬", "万达", "美团", "字节跳动", "大疆", "太平洋保险"]

	# set(open(model_path + "data/all_company.txt").read().split("\n")) - crawling.all_comp

	for k in keys:
		redis_queue.rpush(SEARCH_LINK, crawling.base_url.format(1, k))
	print(len(keys))


def run_search():
	"""调度"""
	while True:
		cos_id = redis_queue.lpop(SEARCH_LINK)
		if cos_id:
			try:
				html = crawling.get_html(cos_id)
				redis_queue.rpush(SEARCH_HTML, html)
			except Exception as e:
				traceback.print_exc()
		else:
			print("search link queue is empty")
			break


def parse_search():
	while True:
		cos_id = redis_queue.lpop(SEARCH_HTML)
		if cos_id:
			try:
				crawling.parse_link_html(cos_id)
			except Exception as e:
				traceback.print_exc()
		else:
			# time.sleep(10)

			if not redis_queue.llen(SEARCH_LINK):
				gevent.sleep(3)
				if not redis_queue.llen(SEARCH_HTML):
					print("search html queue is empty")

					break
			else:
				gevent.sleep(1)


def run_comp():
	"""调度"""
	while True:
		cos_id = redis_queue.lpop(COMP_LINK)
		if cos_id:
			try:
				html = crawling.get_html(cos_id)
				redis_queue.rpush(COMP_HTML, html)
			except Exception as e:
				traceback.print_exc()
		else:
			if not redis_queue.llen(SEARCH_LINK) and not redis_queue.llen(SEARCH_HTML):
				gevent.sleep(5)
				if not redis_queue.llen(COMP_LINK):
					print("company link queue is empty")
					break
			else:
				gevent.sleep(1)


def parse_comp():
	while True:
		cos_id = redis_queue.lpop(COMP_HTML)
		if cos_id:
			try:
				crawling.parse_comp_html(cos_id)
			except Exception as e:
				traceback.print_exc()
		else:
			if not redis_queue.llen(SEARCH_LINK) and not redis_queue.llen(SEARCH_LINK) and not redis_queue.llen(
					COMP_LINK):
				gevent.sleep(9)
				if not redis_queue.llen(COMP_HTML):
					print("company html queue is empty")

					break
			else:
				gevent.sleep(1)


def run_brand():
	"""调度"""
	while True:
		cos_id = redis_queue.lpop(BRAND_LINK)
		if cos_id:
			try:
				html = crawling.get_html(cos_id)
				redis_queue.rpush(BRAND_HTML, html)
			except Exception as e:
				traceback.print_exc()
		else:
			if not redis_queue.llen(SEARCH_LINK) and not redis_queue.llen(SEARCH_HTML) and not redis_queue.llen(
					COMP_LINK) and not redis_queue.llen(COMP_HTML):
				gevent.sleep(24)
				if not redis_queue.llen(BRAND_LINK):
					print("brand link queue is empty")
					break
			else:
				gevent.sleep(1)


def parse_brand():
	while True:
		cos_id = redis_queue.lpop(BRAND_HTML)
		if cos_id:
			try:
				crawling.parse_brand_html(cos_id)
			except Exception as e:
				traceback.print_exc()
		else:
			if not redis_queue.llen(SEARCH_LINK) and not redis_queue.llen(SEARCH_HTML) and not redis_queue.llen(
					COMP_LINK) and not redis_queue.llen(COMP_HTML) and not redis_queue.llen(BRAND_LINK):
				gevent.sleep(50)
				if not redis_queue.llen(BRAND_HTML):
					print("brand html queue is empty")

					break
			else:
				gevent.sleep(1)


def test_parse(url, func):
	html = crawling.get_html(url)
	# print(html)
	func(html)


def gevent_for_html(sr=5, sp=2, hr=8, hp=2, br=2, bp=2):
	import gevent.monkey
	gevent.monkey.patch_all()
	push_key()
	p = Pool(sr + sp + hr + hp + br + bp)
	for i in range(sr):
		p.apply_async(run_search)
	for i in range(sp):
		p.apply_async(parse_search)
	for i in range(hr):
		p.apply_async(run_comp)
	for i in range(hp):
		p.apply_async(parse_comp)
	for i in range(br):
		p.apply_async(run_brand)
	for i in range(bp):
		p.apply_async(parse_brand)
	p.join()


crawling = Crawling()
if __name__ == '__main__':
	# parse_brand()
	# gevent_for_html(sr=20, sp=3, hr=100, hp=5, br=100, bp=20)
	# gevent_for_html()
	# test_parse("https://www.tianyancha.com/company/1143437059", crawling.parse_comp_html)

	# s = time.time()
	# get_data_with_for()
	# print(time.time() - s)
	#
	html = crawling.get_html("https://www.tianyancha.com/company/150041670")
	print(html)
	# print(crawling.parse_comp_html(html))
