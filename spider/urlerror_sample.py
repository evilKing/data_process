#coding:utf-8

from urllib import request, error

try:
	response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.HTTPError as e:
	print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
	print(e.reason)
else:
	print('Request Successfully')



import socket
import urllib.request
import urllib.error

try:
	response = urllib.request.urlopen('https://www.baidu.com', timeout=0.01)
except urllib.error.URLError as e:
	print(type(e.reason))
	if isinstance(e.reason, socket.timeout):
		print('TIME OUT')

# 解析 url
from urllib.parse import urlparse

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(result), result)

# 构造 url
from urllib.parse import urlunparse

data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(urlunparse(data))

# 解析 url，只是把 params 拼接到 path 中
from urllib.parse import urlsplit

result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
print(result)

# 拼接 url，长度必须是 5
from urllib.parse import urlunsplit

data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
print(urlunsplit(data))

# 对右边的 url 利用左边的 url 的 schame/netloc/path 进行补全
from urllib.parse import urljoin

print(urljoin('http://www.baidu.com', 'FAQ.html'))
print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(urljoin('http://www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com#comment', '?category=2'))


# 将词典参数转换成 url
from urllib.parse import urlencode

params = {
	'name': 'germey',
	'age': 22
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)


# 将 url 的参数转回成词典
from urllib.parse import parse_qs

query = 'name=germey&age=22'
print(parse_qs(query))


# 将 url 的参数转换成元组组成的列表
from urllib.parse import parse_qsl

query = 'name=germey&age=22'
print(parse_qsl(query))

# 可将内容转换为 URL 编码格式，防止乱码
from urllib.parse import quote

keyword = '壁纸'
url = 'https://www.baidu.com/s?wd=' + quote(keyword)
print(url)

# quote() 的逆方法，可以对 URL 解码
from urllib.parse import unquote

url = 'https://www.baidu.com/s?wd=%E5%A3%81%E7%BA%B8'
print(unquote(url))




