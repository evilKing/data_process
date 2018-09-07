#coding:utf-8

import unicodedata

file_path = '../dict/en_college.dict'

save_file_path = file_path + ".bak"


lines = []
with open(file_path, 'r') as fr:
    lines = fr.readlines()
    lines = [unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode('utf8').lower().strip() for line in lines if line.strip() != '']
    lines = list(set(lines))
    lines.sort()
    lines = [line + '\n' for line in lines]

fw = open(save_file_path, 'w')
fw.writelines(lines)
fw.flush()
fw.close()
