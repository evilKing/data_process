#coding:utf-8

file_path = '../dict/en_position_title.dict.store_auto'

save_file_path = file_path + ".bak"


lines = []
with open(file_path, 'r') as fr:
    lines = fr.readlines()
    lines = [line.lower().strip() for line in lines if line.strip() != '']
    lines = list(set(lines))
    lines.sort()
    lines = [line + '\n' for line in lines]

fw = open(save_file_path, 'w')
fw.writelines(lines)
fw.flush()
fw.close()
