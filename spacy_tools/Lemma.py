import spacy

nlp = spacy.load('en')

with open("/Users/hulk/Downloads/head_set.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    if line.strip() == '':
        continue
    tokens = nlp(line)
    print(line)
    for token in tokens:
        print(token.lemma_, end=' ')

    print('======================')
