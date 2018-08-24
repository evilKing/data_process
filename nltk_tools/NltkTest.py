from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

word = wordnet_lemmatizer.lemmatize('working', pos='v')
print(word)
