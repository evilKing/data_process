#coding:utf-8
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en')
matcher = PhraseMatcher(nlp.vocab)

terminology_list = ['Barack Obama', 'Angela Merkel', 'Washington, DC.']
patterns = [nlp(text) for text in terminology_list]
matcher.add('TerminologyList', None, *patterns)

doc = nlp(u"German Chancellor Angela Merkel and US President Barack Obama "
          u"converse in the Oval Office inside the White House in Washington, D.C.")
matches = matcher(doc)
print(matches)

