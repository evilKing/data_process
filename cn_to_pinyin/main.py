#coding:utf-8

from pypinyin import pinyin, lazy_pinyin, Style

# 输出拼音
print(pinyin('中信'))

# 启用多音字模式
print(pinyin('中心', heteronym=True))

print(pinyin('中心', style=Style.FIRST_LETTER))


print(pinyin('中心', style=Style.TONE2, heteronym=True))

print(lazy_pinyin('中心'))

print(pinyin('翟偲翀', heteronym=True))

from pypinyin import load_phrases_dict, load_single_dict
# load_phrases_dict({'步履蹒跚': [['bù'], ['lǚ'], ['pán'], ['shān']]})
# load_single_dict({ord('蹒'): 'pán'})
# print(pinyin('步履蹒跚'))

single_sur_dict = {}
phrases_sur_dict = {}
with open('sur_pinyin.dict', 'r') as fr:
    for line in fr.readlines():
        words = line.strip().split('\t')
        if len(words[0]) > 1:
            spys = words[1].split('/')
            phrases_sur_dict[words[0]] = []
            for spy in spys:
                phrases_sur_dict[words[0]].append([spy])
        else:
            single_sur_dict[ord(words[0])] = words[1]

load_phrases_dict(phrases_sur_dict)
load_single_dict(single_sur_dict)

print(pinyin('翟偲翀'))
