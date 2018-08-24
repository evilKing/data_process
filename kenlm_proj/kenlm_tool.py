#coding:utf-8

from spelling_corrector.corrector import spell_corr
import kenlm

model = kenlm.LanguageModel('../dict/en_position.klm')

print(model.score('financial manager', bos = True, eos = True))

pos_dict = '../dict/en_position.dict'
pos_err_dict = '../dict/en_position_title.dict.store_art_error'

err_dict = {}
with open(pos_err_dict, 'r') as fr:
    lines = fr.readlines()
    lines = [line.lower().strip() for line in lines if line.strip() != '']
    lines = list(set(lines))
    lines.sort()
    for line in lines:
        words = line.split()
        err_dict[words[0]] = words[1]

lines = []
with open(pos_dict, 'r') as fr:
    lines = fr.readlines()
    lines = [line.lower().strip() for line in lines if line.strip() != '']
    lines = list(set(lines))
    lines.sort()

answer_lines = []
cor_count = 0
err_count = 0
for li, line in enumerate(lines):
    words = line.split()
    if words[-1] in err_dict:
        suggests = spell_corr.suggest_word_spelling(words[-1])

        cal_res = []
        for si, sug in enumerate(suggests):
            temp_line = ' '.join(words[:-1]) + ' ' + sug
            val = model.score(temp_line, bos=True, eos=True)
            cal_res.append((si, sug, val))

        cal_res.sort(key=lambda x: x[2], reverse=True)

        flag = False
        if cal_res[0][1].lower() == err_dict[words[-1]].lower():
            cor_count += 1
            flag = True
        else:
            err_count += 1

        answer_lines.append(str(flag) + '\t' + line + '\t' + ' '.join(words[:-1]) + ' ' + cal_res[0][1].lower() + '\t' + err_dict[words[-1]].lower() + '\n')

        # print(flag, '\t', ' '.join(words[:-1]) + ' ' + cal_res[0][1])

save_path = pos_dict + '.spelling'
fw = open(save_path, 'w')
fw.writelines(answer_lines)
fw.flush()
fw.close()

print('ratio: ', float(cor_count)/(cor_count + err_count))