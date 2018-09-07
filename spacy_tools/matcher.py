#coding:utf-8
import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en')
matcher = Matcher(nlp.vocab)

pattern = [{'LOWER': 'hello'}, {'LOWER': 'world'}, {'IS_PUNCT': True}]
matcher.add('HelloWorld', None, pattern)

doc = nlp(u'Hello, world! Hello world!')
matches = matcher(doc)
print(matches)
print(doc[matches[0][1]:matches[0][2]])


matcher.add('HelloWorld', None,
            [{'LOWER': 'hello'}, {'IS_PUNCT': True}, {'LOWER': 'world'}],
            [{'LOWER': 'hello'}, {'LOWER': 'world'}])
matches = matcher(doc)
print(matches)


doc = nlp(u'user name:hulk')
matcher.add('Name', None,
            [{'ORTH': 'user'}, {'ORTH': 'name'}, {'ORTH':':'}, {}])
matches = matcher(doc)
print(matches)
print(doc[matches[0][1]:matches[0][2]])



EVENT = nlp.vocab.strings['EVENT']

def add_event_ent(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    doc.ents += ((EVENT, start, end),)

matcher.add('GoogleIO', add_event_ent,
            [{'ORTH': 'Google'}, {'UPPER': 'I'}, {'ORTH': '/'}, {'UPPER': 'O'}],
            [{'ORTH': 'Google'}, {'UPPER': 'I'}, {'ORTH': '/'}, {'UPPER': 'O'}, {'IS_DIGIT': True}]
            )

BAD_HTML_FLAG = nlp.vocab.add_flag(lambda text: False)

def merge_and_flag(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start: end]
    span.merge(is_stop=True)
    span.set_flag(BAD_HTML_FLAG, True)

matcher.add('BAD_HTML', merge_and_flag,
            [{'ORTH': '<'}, {'LOWER': 'br'}, {'ORTH': '>'}],
            [{'ORTH': '<'}, {'LOWER': 'br/'}, {'ORTH': '>'}])
