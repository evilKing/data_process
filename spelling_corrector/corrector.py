#coding:utf-8

import logging
import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import get_tokenizer

'''
参考：
1. https://www.jianshu.com/p/96c01666aeeb
2. https://blog.csdn.net/qq_27879381/article/details/63351483
'''
class Spelling_Corrector(object):

    def __init__(self, language="en_US"):
        if not enchant.dict_exists(language):
            logging.warning("Spelling_Corrector: Don't have {} , Please check it!!!", language)
            logging.warning("Recommend same language for you: {}", enchant.list_languages())
            language = "en_US"
        self.dict = enchant.Dict(language)
        self.check = SpellChecker(language)
        self.tokenizer = get_tokenizer(language)

    def is_word_spelling_corrector(self, word):
        '''检查单词是否拼写正确'''

        return self.dict.check(word)

    def suggest_word_spelling(self, word):
        '''推荐可能的单词拼写'''

        return self.dict.suggest(word)

    def word_spelling_corrector(self, word):
        '''推荐最可能的单词拼写'''

        if self.is_word_spelling_corrector(word):
            return word

        pending_words = self.suggest_word_spelling(word)

        return pending_words[0] if len(pending_words) > 0 else word

    def sentence_spelling_corrector(self, sentence):
        '''对句子单词进行拼写检查，输出拼写错误单词'''

        self.check.set_text(sentence)
        return [("ERROR", err.word) for err in self.check]

spell_corr = Spelling_Corrector()

if __name__ == '__main__':
    f = spell_corr.suggest_word_spelling('vender')
    print(f)

    # f = spell_corr.is_word_spelling_corrector('he lo')
    # print(f)


