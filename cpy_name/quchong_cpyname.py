#coding:utf-8
import re

org_cpy_name_path = '/Users/hulk/Workspace/PycharmProjects/cmpname/data/en_company_weak_store.dict'

space_pat = re.compile(' {4,}.*')

lines = set()
with open(org_cpy_name_path, 'r') as fr:
    for line in fr.readlines():
        if line.strip() == '' or '<' in line:
            continue
        flag = False
        for i in range(1990, 2019):
            temp = str(i) + '-'
            if temp in line:
                flag = True
        if flag:
            continue
        line = space_pat.sub('', line)
        line = line.strip() + '\n'
        lines.add(line)

save_cpy_name_path = '/Users/hulk/Workspace/PycharmProjects/cmpname/data//en_company_weak_verify.dict'
fw = open(save_cpy_name_path, 'w')
lines = list(lines)
lines.sort()
fw.writelines(lines)
fw.flush()
fw.close()

