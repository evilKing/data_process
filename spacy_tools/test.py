#coding:utf-8
import spacy

spacy_nlp_en = spacy.load('en')

text = u'             SHENZHEN INSTITUTE OF ADVANCED TECHNOLOGY,CHINESE ACADEMY OF SCIENCES,        '
text = u'aaaaa'

# doc = spacy_nlp_en(text)
#
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)
#


doc = spacy_nlp_en(text)

for chunk in doc.noun_chunks:
    print(chunk.text + "####", chunk.root.text, chunk.root.dep_, chunk.root.head.text)



doc = spacy_nlp_en(text)

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


