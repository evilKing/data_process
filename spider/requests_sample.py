#coding:utf-8

import requests

# r = requests.get('https://www.baidu.com/')
# print(type(r))
# print(r.status_code)
# print(type(r.text))
# print(r.text)
# print(r.cookies)
#
# r = requests.post('http://httpbin.org/post')
# r = requests.put('http://httpbin.org/put')
# r = requests.delete('http://httpbin.org/delete')
# r = requests.head('http://httpbin.org/get')
# r = requests.options('http://httpbin.org/get')

data = {
	'name': 'germey',
	'age' : 22
}
r = requests.get('http://httpbin.org/get', params=data)
print(r.text)
print(r.json())
print(type(r.json()))

print('=================================')

import re

headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get('https://www.zhihu.com/explore', headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles = re.findall(pattern, r.text)
print(titles)

print('===========================')

# r = requests.get('https://github.com/favicon.ico')
# print(r.text)
# print(r.content)
# with open('favicon.ico', 'wb') as f:
# 	f.write(r.content)

print('=========================')

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get('https://www.zhihu.com/explore', headers=headers)
print(r.text)


print('=======================')

data = {'name': 'germey', 'age': '22'}
r = requests.post('http://httpbin.org/post', data=data)
print(r.text)

print('=======================')

# r = requests.get('http://www.jianshu.com')
# print(type(r.status_code), r.status_code)
# print(type(r.headers), r.headers)
# print(type(r.cookies), r.cookies)
# print(type(r.url), r.url)
# print(type(r.history), r.history)
#
# exit() if not r.status_code == requests.codes.ok else print('Request Successfully')


print('=======================')

# files = {'file': open('favicon.ico', 'rb')}
# r = requests.post('http://httpbin.org/post', files=files)
# print(r.text)

r = requests.get('https://www.baidu.com')
print(r.cookies)
for key, value in r.cookies.items():
	print(key + '=' + value)

print('==========================')

headers = {
	'Cookie': 'q_c1=31653b264a074fc9a57816d1ea93ed8b|1474273938000|1474273938000; d_c0="AGDAs254kAqPTr6NW1U3XTLFzKhMPQ6H_nc=|1474273938"; __utmv=51854390.100-1|2=registration_date=20130902=1^3=entry_date=20130902=1;a_t="2.0AACAfbwdAAAXAAAAso0QWAAAgH28HQAAAGDAs254kAoXAAAAYQJVTQ4FCVgA360us8BAklzLYNEHUd6kmHtRQX5a6hiZxKCynnycerLQ3gIkoJLOCQ==";z_c0=Mi4wQUFDQWZid2RBQUFBWU1DemJuaVFDaGNBQUFCaEFsVk5EZ1VKV0FEZnJTNnp3RUNTWE10ZzBRZFIzcVNZZTFGQmZn|1474887858|64b4d4234a21de774c42c837fe0b672fdb5763b0',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}
r = requests.get('https://www.zhihu.com', headers=headers)
print(r.text)

print('==========================')

import requests.cookies

cookies = 'q_c1=31653b264a074fc9a57816d1ea93ed8b|1474273938000|1474273938000; d_c0="AGDAs254kAqPTr6NW1U3XTLFzKhMPQ6H_nc=|1474273938"; __utmv=51854390.100-1|2=registration_date=20130902=1^3=entry_date=20130902=1;a_t="2.0AACAfbwdAAAXAAAAso0QWAAAgH28HQAAAGDAs254kAoXAAAAYQJVTQ4FCVgA360us8BAklzLYNEHUd6kmHtRQX5a6hiZxKCynnycerLQ3gIkoJLOCQ==";z_c0=Mi4wQUFDQWZid2RBQUFBWU1DemJuaVFDaGNBQUFCaEFsVk5EZ1VKV0FEZnJTNnp3RUNTWE10ZzBRZFIzcVNZZTFGQmZn|1474887858|64b4d4234a21de774c42c837fe0b672fdb5763b0'
jar = requests.cookies.RequestsCookieJar()
headers = {
	'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
for cookie in cookies.split(';'):
	key, value = cookie.split('=', 1)
	jar.set(key, value)
r = requests.get('http://www.zhihu.com', cookies=jar, headers=headers)
print(r.text)

print('======================')

s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)

print('======================')

response = requests.get('https://www.12306.cn')
print(response.status_code)

print('======================')

# proxies = {
# 	"http": "http://10.10.1.10:3128",
# 	"https": "http://10.10.1.10:1080",
# }
# requests.get('https://www.taobao.com', proxies=proxies)

print('======================')

r = requests.get('https://www.taobao.com', timeout=1)
print(r.status_code)

print('======================')

# from requests.auth import HTTPBasicAuth
#
# r = requests.get('http://localhost:5000', auth=HTTPBasicAuth('username', 'password'))
# print(r.status_code)
# r = requests.get('http://localhost:5000', auth=('username', 'password'))
# print(r.status_code)
#
# from requests_oauthlib import OAuth1
#
# url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
# auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
#               'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
# requests.get(url, auth=auth)

from requests import Request, Session

url = 'http://httpbin.org/post'
data = {
	'name': 'germey'
}
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
s = Session()
req = Request('POST', url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)
print(r.text)
