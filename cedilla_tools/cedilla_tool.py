#coding:utf-8

import unicodedata

line = u'École Normale Supérieure de Lyon'
ans_line = unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode('utf8')

print(ans_line)

