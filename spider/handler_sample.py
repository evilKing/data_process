#coding:utf-8

from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from urllib.error import URLError

# 登陆认证
username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
	result = opener.open(url)
	html = result.read().decode('utf-8')
	print(html)
except URLError as e:
	print(e.reason)


from urllib.request import ProxyHandler, build_opener
# 代理
proxy_handler = ProxyHandler({
	'http': 'http://127.0.0.1:9743',
	'https': 'https://127.0.0.1:9743'
})
opener = build_opener(proxy_handler)
try:
	response = opener.open('https://www.baidu.com')
	print(response.read().decode('utf-8'))
except URLError as e:
	print(e.reason)


import http.cookiejar, urllib.request
# Cookies

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
	print(item.name+"="+item.value)

# 将 Cookies 存成文件
filename = 'cookies.txt'
# cookie = http.cookiejar.LWPCookieJar(filename)    # 可将 Cookie 保存成 libwww-perl 格式
cookie = http.cookiejar.MozillaCookieJar(filename)  # 可将 Cookie 保存成 Mozilla型浏览器的 cookie 形式
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)


# 读取 cookie 文件
cookie = http.cookiejar.LWPCookieJar()
cookie.load('cookies.txt', ignore_expires=True, ignore_discard=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
print(response.read().decode('utf-8'))

