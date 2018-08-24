#coding:utf-8

from spelling_corrector.corrector import spell_corr
import kenlm

model = kenlm.LanguageModel('../dict/en_position.klm')

pos_dict = '../dict/en_position.dict'
pos_err_dict = '../dict/en_position_title.dict.store_art_error'

save_path = pos_dict + '.save'

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

corr_lines = []
cor_count = 0
err_count = 0
for li, line in enumerate(lines):
    words = line.split()
    if spell_corr.is_word_spelling_corrector(words[-1]) \
            or '/' in words[-1] or '-' in words[-1]:
        corr_lines.append(line + '\n')
    elif words[-1] in err_dict:
        suggests = spell_corr.suggest_word_spelling(words[-1])

        cal_res = []
        for si, sug in enumerate(suggests):
            temp_line = ' '.join(words[:-1]) + ' ' + sug
            val = model.score(temp_line, bos=True, eos=True)
            cal_res.append((si, sug, val))

        cal_res.sort(key=lambda x: x[2], reverse=True)

        corr_lines.append(' '.join(words[:-1]) + ' ' + cal_res[0][1].lower() + '\n')

        cor_count += 1
    else:
        err_count += 1
        print(line)

corr_lines = [line.lstrip() for line in corr_lines]
corr_lines = list(set(corr_lines))
corr_lines.sort()

fw = open(save_path, 'w')
fw.writelines(corr_lines)
fw.flush()
fw.close()

print('ratio: ', cor_count/float(len(lines)), cor_count, err_count)


