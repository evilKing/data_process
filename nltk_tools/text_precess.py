#coding:utf-8

text = '''
A dedicated and self-motivated professional with extensive B2B working experience in multi-national
environment. Qualified to postgraduate degree level and CIM registered (MCIM), able to demonstrate an
excellent working knowledge of the marketing mixes & techniques. Possesses excellent interpersonal,
communication and negotiation skills and the ability to develop and maintain mutually beneficial internal
and external relationships. Enjoys being part of a successful and productive team, and thrives in highly
pressurised and challenging working environments.
'''

from nltk.tokenize import word_tokenize, sent_tokenize

words = word_tokenize(text)
# print(words)

sentences = sent_tokenize(text)
# print(sentences)

from nltk.corpus import stopwords

stop_word_list = stopwords.words("english")

words = [w for w in words if w not in stop_word_list]
# print(words)

from nltk import pos_tag

sentence = word_tokenize("I always lie down to tell a lie.")
tags = pos_tag(sentence)
# print(tags)

import nltk

my_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")
parser = nltk.ChartParser(my_grammar)

sentence = word_tokenize("I shot an elephant in my pajamas")
for tree in parser.parse(sentence):
    print(tree)
    # tree.draw()

from nltk import pos_tag, ne_chunk

chunk_list = ne_chunk(pos_tag(word_tokenize("Antonio joined Udacity Inc. in California.")))
print(chunk_list)

