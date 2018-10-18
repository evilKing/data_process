#coding:utf-8
import spacy

spacy_nlp_en = spacy.load('en_core_web_sm')


def token_by_lemmatize(text):
    tokens = spacy_nlp_en(text)
    for token in tokens:
        print(token, token.lemma_, token.lemma)

def token_by_pos(text):
    tokens = spacy_nlp_en(text)
    for token in tokens:
        print(token, token.pos_, token.pos)
    return

def token_by_pos_extract_v(text):
    '''抽取动词'''

    tokens = spacy_nlp_en(text)
    tokens = list(filter(lambda token: token.tag_.startswith('V'), tokens))
    return [(token.text, token.pos, token.pos_) for token in tokens]

def token_by_ner(text):
    tokens = spacy_nlp_en(text)
    for ent in tokens.ents:
        print(ent, ent.label_, ent.label)

def token_by_extra_phrase(text):
    tokens = spacy_nlp_en(text)
    for np in tokens.noun_chunks:
        print(np)

def ftool():
    file_path = '../resume/000AAA.txt'

    lines = []
    with open(file_path, 'r') as fr:
        lines = fr.readlines()
        lines = [line.strip() for line in lines if line.strip() != '']

    return lines

if __name__ == '__main__':
    text = '''Asynchronous and nested-parallel programming model for big data analytics, sponsored by NFS of Guangdong Province. 2'''
    token_by_pos(text)
    # token_by_ner(text)
    # token_by_extra_phrase(text)

    # for li, line in enumerate(ftool()):
    #     sentence = []
    #     for (token, pos, pos_) in token_by_pos_extract_v(line):
    #         sentence.append((li, token, pos_))
    #     print(sentence)