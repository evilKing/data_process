import spacy

nlp = spacy.load('en_core_web_lg')


nlp = spacy.load('en_core_web_lg')

doc1 = nlp(u"Language: SAS, SQL, R, STATA, SPSS")
doc2 = nlp(u"Language: English, Mandarin")
doc3 = nlp(u"Language: English(fluent), Mandarin(proficiency)")

for doc in [doc1, doc2, doc3]:
    for other_doc in [doc1, doc2, doc3]:
        print(doc.similarity(other_doc), doc, other_doc, end='\t')
    print('\n')


