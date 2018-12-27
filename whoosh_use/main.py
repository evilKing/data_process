#coding:utf-8


import os.path

from whoosh import fields
from whoosh import index
import jieba

lines = [
    '东方不亮西方亮，二逼啥样儿你啥样儿。',
    '想必一定是人渣中的极品，禽兽中的禽兽。看看啊，你这小脸瘦得，都没个猪样啦！',
    '因为所以，科学道理；不但而且，我是恁爹。看你玉树临风，英俊潇洒，风流倜傥，人见人爱，花见花开。',
    '别以为比我年轻你就能多蹦几天，棺材装的是死人不是老人！',
    '别以为比我年轻你就能多蹦踏几天，棺材里边装的事装的是死人不是老人！'
]

schema = fields.Schema(keyword=fields.TEXT(stored=True), index=fields.ID(stored=True), content=fields.TEXT(stored=True))

if not os.path.exists("index"):
    os.mkdir('index')

ix = index.create_in('index', schema)
ix = index.open_dir('index')

writer = ix.writer()
# writer.add_document(keyword='my document', content='this is my document')
# writer.add_document(keyword='my second document', content='this is my second document')

for li, line in enumerate(lines):
    for word in list(jieba.cut(line)):
        print(word)
        writer.add_document(keyword=word, content=line, index=str(li))

writer.commit()

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser('keyword', ix.schema).parse('老人')
    result = searcher.search(query)
    # print("=======================" + result)
    for res in result:
        print(res)



