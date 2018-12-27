#coding:utf-8

import requests
import re, time


proxy = {
			"http:": "127.0.0.1:1087",
			"https": "127.0.0.1:1087"
		}

py_dict = {}
pinyin_pat = re.compile('lang="pinyin">(?P<py>.+?)<')
sur_pat = re.compile('href="(?P<url>.+?)".+?title="(?P<sur>[一-龥]+)姓')


url = 'https://zh.wikipedia.org/wiki/%E7%99%BE%E5%AE%B6%E5%A7%93'
html = requests.get(url, proxies=proxy, timeout=5)
html.encoding="utf-8"
# print(html.text)

mats = sur_pat.findall(html.text)
for mat in mats:
    if len(mat[1]) > 4 or mat[1] in ['百家', '中国', '漢'] or 'Template' in mat[0] or '(' in mat[0] or 'php' in mat[0]:
        continue
    # print('https://zh.wikipedia.org' + mat[0], mat[1])
    py_dict[mat[1]] = 'https://zh.wikipedia.org' + mat[0]

sur_py_lines = []
for sur, url in py_dict.items():
    html = requests.get(url, proxies=proxy, timeout=5)
    html.encoding = "utf-8"
    mat = pinyin_pat.search(html.text)
    if mat and 'py' in mat.groupdict() and mat.group('py'):
        print(sur + '\t' + mat.group('py'))
        sur_py_lines.append(sur + '\t' + mat.group('py') + '\n')

fw = open('sur_pinyin.dict', 'w')
fw.writelines(sur_py_lines)
fw.flush()
fw.close()






