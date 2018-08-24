#coding:utf-8

from google_translation.translate import gtran
from spelling_corrector.corrector import spell_corr

file_path = '../dict/en_position.dict'
save_file_path = file_path + ".store"

lines = []
with open(file_path, 'r') as fr:
    lines = fr.readlines()
    lines = [line.strip() for line in lines if line.strip() != '']


if __name__ == '__main__':
    cn_lines = []
    for li, line in enumerate(lines):
        # cn_line = gtran.translate(line)
        cn_line = spell_corr.sentence_spelling_corrector(line)
        if len(cn_line) > 0:
            print(li, '\t', line, "\t\t", cn_line)
            cn_lines.append(line + '\n')

    fw = open(save_file_path, 'w')
    fw.writelines(cn_lines)
    fw.flush()
    fw.close()

