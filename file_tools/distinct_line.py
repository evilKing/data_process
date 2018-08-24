#coding:utf-8

from spelling_corrector.corrector import spell_corr

file_path = '../dict/en_position_title.txt'

file2 = '/Users/hulk/Workspace/sourcetree/resume_models_dicts/data/dict/en_position_title.dict'
save_file_path = file2 + ".store_little1"


lines = []
with open(file_path, 'r') as fr:
    lines = fr.readlines()
    lines = [line.strip() for line in lines if line.strip() != '']
    lines = list(set(lines))

right_lines = []
with open(file2, 'r') as fr:
    right_lines = fr.readlines()
    right_lines = [line.strip() for line in right_lines if line.strip() != '']
    right_lines = list(set(right_lines))

last_lines = []
for line in right_lines: # 我
    if line not in lines or not spell_corr.is_word_spelling_corrector(line):   # 他
        continue
    last_lines.append(line + '\n')

last_lines.sort()

fw = open(save_file_path, 'w')
fw.writelines(last_lines)
fw.flush()
fw.close()



