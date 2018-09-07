#coding:utf-8
import spacy

spacy_nlp_en = spacy.load('en')

doc = spacy_nlp_en(u'Apple is looking at buying U.K. startup for $1 billion')

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)



doc = spacy_nlp_en(u'Autonomous cars shift insurance liability toward manufacturers')

for chunk in doc.noun_chunks:
    print(chunk.text + "####", chunk.root.text, chunk.root.dep_, chunk.root.head.text)



doc = spacy_nlp_en(u'Apple is looking at buying U.K. startup for $1 billion')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


