#coding:utf-8
import spacy

nlp = spacy.load('en')

filename = '../dict/hotelreviews.txt'
document = open(filename, 'rb').read().decode('utf8')

document = nlp(document)
print(dir(document))

# Tokenization
print(document[0])

# 列出 document 中的句子
print(list(document.sents))


# 词性标注

# 获得所有标注
all_tags = {w.pos: w.pos_ for w in document}
print(all_tags)

# document 中第一个句子的词性标注
for word in list(document.sents)[0]:
    print(word, word.tag_)

# 数据清洗，并统计 token 词频取前 top 5
noisy_pos_tags = ['PROP']
min_token_length = 2

# 检查 token 是不是噪音的函数
def isNoise(token):
    is_noise = False
    if token.pos_ in noisy_pos_tags:
        is_noise = True
    elif token.is_stop == True:
        is_noise = True
    elif len(token.string) <= min_token_length:
        is_noise = True

    return is_noise

def cleanup(token, lower=True):
    if lower:
        token = token.lower()

    return token.strip()

from collections import Counter
cleaned_list = [cleanup(word.string) for word in document if not isNoise(word)]
print(Counter(cleaned_list).most_common(5))


# 实体识别
labels = set([w.label_ for w in document.ents])
for label in labels:
    entities = [cleanup(e.string, lower=False) for e in document.ents if label == e.label_]
    entities = list(set(entities))
    print(label, entities)


# 依存句法分析
hotel = [sent for sent in document.sents if 'hotel' in sent.string.lower()]

sentence = hotel[2]
# 创建依存树
for word in sentence:
    print(word, ': ', str(list(word.children)))


'''
解析所有居中包含“hotel”单词的句子的依存关系，
并检查对于 hotel 人们用了哪些形容词。
我创建了一个自定义函数，用于分析依存关系并进行相关的词性标注。
'''
character = 'hotel'
def pos_words(sentence, token, ptag):
    sentences = [sent for sent in sentence.sents if token in sent.string]
    pwrds = []
    for sent in sentences:
        for word in sent:
            if character in word.string:
                pwrds.extend(
                    [child.string.strip() for child in word.children
                     if child.pos_ == ptag])

    return Counter(pwrds).most_common(10)

print(pos_words(document, 'hotel', 'adj'))



# 生成名词短语
doc = nlp('I love data science on analytics vidhya')
for np in doc.noun_chunks:
    print(np.text, np.root.dep_, np.root.head.text)


# 集成词向量

from numpy import dot
from numpy.linalg import norm
from spacy.lang.en import English
parser = English()

apple = parser.vocab['apple']
cosine = lambda v1, v2: dot(v1, v2)/(norm(v1)*norm(v2))
others = list({w for w in parser.vocab if w.has_vector and w.orth_.islower() and w.lower_ != 'apple'})



