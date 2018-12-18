#coding:utf-8

from os.path import dirname, abspath, join
dict_root_path = join(dirname(dirname(abspath(__file__))), 'dict')

en_company_path = join(dict_root_path, 'en_company.dict')

# 加载强公司后缀
company_suffix_path = join(dict_root_path, 'company_suffix.dict')
company_suffix = set()
with open(company_suffix_path, 'r') as fr:
	suffixs = fr.readlines()
	suffixs = [line.strip() for line in suffixs]
	company_suffix = set(suffixs)

# 加载弱公司后缀
weak_company_suffix_path = join(dict_root_path, 'weak_company_suffix.dict')
weak_company_suffix = set()
with open(weak_company_suffix_path, 'r') as fr:
	suffixs = fr.readlines()
	suffixs = [line.strip() for line in suffixs]
	weak_company_suffix = set(suffixs)

strong_company_list = []
weak_company_list = []
company_abbreviation_list = []

with open(en_company_path, 'r') as fr:
	i = 0
	for line in fr:
		line = line.strip()
		words = line.split()
		if len(words) < 10 and any([line.endswith(suffix) for suffix in company_suffix]):
			strong_company_list.append(line + '\n')
		elif len(words) < 10 and any([line.endswith(suffix) for suffix in weak_company_suffix]):
			weak_company_list.append(line + '\n')
		else:
			company_abbreviation_list.append(line + '\n')
		if i % 2000 == 0:
			print(line, '\t', i)
		i += 1

company_path = join(dict_root_path, 'en_company_strong.dict')
fw = open(company_path, 'w')
strong_company_list.sort()
fw.writelines(strong_company_list)
fw.flush()
fw.close()

company_weak_path = join(dict_root_path, 'en_company_weak.dict')
fw = open(company_weak_path, 'w')
weak_company_list.sort()
fw.writelines(weak_company_list)
fw.flush()
fw.close()

weak_company_path = join(dict_root_path, 'en_weak_company.dict')
fw = open(weak_company_path, 'w')
company_abbreviation_list.sort()
fw.writelines(company_abbreviation_list)
fw.flush()
fw.close()



