#coding:utf-8

import requests
import os
from pyquery import PyQuery
import re, time, copy, json
from multiprocessing import Pool, cpu_count
from gevent import monkey
from gevent.pool import Pool as ge_pool
from gevent.queue import Queue


class SpiderTool(object):
    monkey.patch_socket()
    proxies_queue = Queue(100)
    # process_pool = Pool(processes=cpu_count())

    def __init__(self, parser, output, cookies = None):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        self.cookies = cookies if cookies else {'cookie': 'UM_distinctid=167557452b5f6-0b4644e0763f48-35627400-13c680-167557452b6377; _ga=GA1.2.392079514.1543326947; cloud-anonymous-token=d8246fe4f0324e40aa514643feff8b75; _gid=GA1.2.1493862284.1543630829; cloud-sso-token=DEB1E1ADE4CE73FE0651C7071646607B; _gat=1'}
        self.parser = parser
        self.output = output

    def proxy_producer(self):
        ip_url = 'http://193.112.31.15:5000/proxy'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        response = requests.get(ip_url, headers=headers, timeout=5)
        ips = json.loads(response.text)
        for ip in ips:
            proxies = {
                'http': 'http://' + ip,
                'https': 'http://' + ip,
            }
            if not self.proxies_queue.full():
                self.proxies_queue.put_nowait(proxies)

    def crawling_web(self, url):
        # try:
            if self.proxies_queue.empty():
                self.proxy_producer()
            proxies = self.proxies_queue.get_nowait()
            res = requests.get(url, headers=self.headers, cookies=self.cookies, proxies=proxies, timeout=10)

            ans_list, new_urls = self.parser.parse(res)
            if new_urls:
                self.scheduler(new_urls)
            if ans_list:
                self.output.process(ans_list)
        # except:
        #     failed_urls.append(url)
        #     print('fali to crawle {}'.format(url))

    def greenlet_crawler(self, urls):
        greenlet_pool = ge_pool(10)
        for url in urls:
            greenlet_pool.apply_async(self.crawling_web, (url, ))
        greenlet_pool.join()

    def split_urls(self, urls):
        if not urls:
            print('no url in urls')
            return [urls]
        num_urls = len(urls)
        num_cpus = cpu_count()
        if num_urls < num_cpus:
            return [urls]
        num_urls_per_cpu = int(num_urls / num_cpus)
        splitted_urls = []
        for i in range(num_cpus):
            if i == 0:
                splitted_urls.append(urls[: (i + 1) * num_urls_per_cpu])
            elif i == num_cpus - 1:
                splitted_urls.append(urls[i * num_urls_per_cpu:])
            else:
                splitted_urls.append(urls[i * num_urls_per_cpu: (i + 1) * num_urls_per_cpu])

        return splitted_urls

    def scheduler(self, urls):
        global failed_urls
        failed_urls = []
        splitted_urls = self.split_urls(urls)
        # global process_pool
        if not hasattr(self, 'process_pool'):
            self.process_pool = Pool(processes=cpu_count())
        for urls in splitted_urls:
            self.process_pool.map(self.crawling_web, urls)  #.apply_async(self.greenlet_crawler, (urls,))
        self.process_pool.close()
        self.process_pool.join()
        if not failed_urls:
            # self.scheduler(copy.deepcopy(failed_urls))
            self.output.fail_process(failed_urls)

class ItemParser(object):

    def __init__(self):
        self.formerly_pat = re.compile('(?<=formerly:)[a-z0-9,.\s]+(?=\(filings)', re.I)
        self.start_num_pat = re.compile('[0-9]+')
        self.cpy_list = []
        self.new_urls = []

    def clean(self):
        self.cpy_list.clear()
        self.new_urls.clear()

    def parse(self, res):
        self.clean()

        doc = PyQuery(res.text)
        url = res.url

        container = doc('#contentDiv')
        # 提取公司名
        tds = container('td').items()
        for td in tds:
            if td.attr('valign'):
                continue
            html_str = td.html()
            if not html_str:
                continue
            lidx = html_str.find('<br/>')
            if lidx:
                # print(html_str[:lidx])
                self.cpy_list.append(html_str[:lidx])
                mat = self.formerly_pat.search(html_str)
                if mat:
                    # print(mat.group().strip())
                    self.cpy_list.append(mat.group().strip())
        if not self.cpy_list:
            return self.cpy_list, self.new_urls

        # 检测是否还有其他页
        input_list = list(container('form').items())
        if input_list:
            click_val = input_list[-1]('input').attr('onclick')
            if click_val:
                cgi_idx = click_val.find('/cgi-bin')
                click_val = 'https://www.sec.gov' + click_val[cgi_idx:-1]
                # print(click_val)
                url_idx = url.find('start=')
                start_idx = click_val.find('start=')
                if url_idx < 0:
                    temp_url = click_val[:start_idx] + 'start=' + str(0) + '&count=100&hidefilings=0'
                else:
                    start_mat = self.start_num_pat.search(url[start_idx:])
                    start_num = int(start_mat.group()) + 100
                    temp_url = click_val[:start_idx] + 'start=' + str(start_num) + '&count=100&hidefilings=0'

                self.new_urls.append(temp_url)

        return self.cpy_list, self.new_urls

class AnsOutput(object):
    def __init__(self, save_path):
        self.save_path = save_path

    def open(self):
        self.fw = open(self.save_path, 'a')

    def process(self, cpy_list):
        self.fw.writelines(cpy_list)
        self.fw.flush()

    def fail_process(self, urls):
        for url in urls:
            print('error: ', url)

    def close(self):
        self.fw.flush()
        self.fw.close()


class CompanyHandler(object):

    def __init__(self, src_path, save_path):
        self.src_path = src_path
        self.save_path = save_path

    def handler(self):
        output = AnsOutput(save_path)
        output.open()
        parser = ItemParser()
        spider = SpiderTool(parser, output)
        spider.scheduler(self.generate_urls())
        output.close()

    def generate_urls(self):
        company_name_list = set()
        with open(self.src_path, 'r') as fr:
            for line in fr:
                for word in line.split():
                    company_name_list.add(word)

        urls = []
        for word in company_name_list:
            urls.append('https://www.sec.gov/cgi-bin/browse-edgar?company=' + word + '&owner=exclude&action=getcompany')
        return urls

# test_url = 'https://www.sec.gov/cgi-bin/browse-edgar?company=RAINES&owner=exclude&action=getcompany'
# query_company_name(test_url)

if __name__ == '__main__':
    src_path = '/Users/hulk/Workspace/PycharmProjects/data_process/dict/en_company_weak.dict'
    save_path = '/Users/hulk/Workspace/PycharmProjects/data_process/dict/en_company_weak_verify.dict'
    handler = CompanyHandler(src_path, save_path)
    handler.handler()