#coding:utf-8

company_list = set()
with open('/Users/hulk/Workspace/PycharmProjects/data_process/dict/en_company_weak_verify.dict', 'r') as fr:
    for line in fr:
        company_list.add(line)
    company_list = [line for line in company_list if line.strip() != '']

fw = open('/Users/hulk/Workspace/PycharmProjects/data_process/dict/en_company_weak_verify.dict', 'w')
fw.writelines(company_list)
fw.flush()
fw.close()

