#coding:utf-8

from spelling_corrector.corrector import spell_corr
from google_translation.translate import gtran
from google_translation.baidu_translator import baidu_corr
from autocorrect import spell

start_index = 3171

def read_lines(file_path):
    lines = []
    with open(file_path, 'r') as fr:
        lines = fr.readlines()
        lines = [line.strip() for line in lines if line.strip() != '']
        lines = list(set(lines))
        lines.sort()
    return lines[start_index:]

# 对每行进行纠错 + 人工筛选

def spell_by_auto(lines, save_path):
    corr_lines = []
    fw = open(save_path + '.store_auto', 'a')

    for line in lines:
        corr_line = spell(line)
        corr_lines.append(corr_line.lower() + '\n')

        print(corr_line)

    corr_lines = list(set(corr_lines))
    corr_lines.sort()

    fw.writelines(corr_lines)
    fw.flush()
    fw.close()
    print('纠错完毕!!!')


def spell_by_artificail(lines, save_path):
    corr_lines = []
    fw = open(save_path + '.store_art', 'a')
    fw_err = open(save_path + '.store_art_error', 'a')

    for li, line in enumerate(lines):
        if spell_corr.is_word_spelling_corrector(line):
            corr_lines.append(line + '\n')
            fw.write(line + '\n')
            fw.flush()
            continue
        pendings = spell_corr.suggest_word_spelling(line)

        if len(pendings) == 0:
            fw_err.write(line + '\t\n')
            fw_err.flush()
            continue
        elif len(pendings) == 1:
            corr_lines.append(pendings[0] + '\n')
            fw.write(pendings[0] + '\n')
            fw.flush()

            fw_err.write(line + "\t" + pendings[0] + '\n')
            fw_err.flush()
            continue

        tran_pendings = [(i, pending, gtran.translate(pending)) for i, pending in enumerate(pendings)]
        # tran_pendings = [(i, pending, baidu_corr.translate(pending)) for i, pending in enumerate(pendings)]

        print(li + start_index, line, gtran.translate(line))
        print(tran_pendings)

        val = input()
        index = int(0 if val == '' else val)
        while index < -3 or index >= len(pendings):
            print('Please input again!')
            val = input()
            index = int(0 if val == '' else val)

            if index == -4:
                print('continue....')
                break
        if index == -1:
            continue
        if index == -2:
            break
        if index == -3:
            corr_lines.append(line + '\n')
            fw.write(line + '\n')
            fw.flush()
            continue

        corr_lines.append(pendings[int(index)] + '\n')
        fw.write(pendings[int(index)] + '\n')
        fw.flush()

        fw_err.write(line + "\t" + pendings[int(index)] + '\n')
        fw_err.flush()

    corr_lines = list(set(corr_lines)).sort()

    fw.writelines(corr_lines)
    fw.flush()
    fw.close()

    print(corr_lines)

    print('纠错完毕!!!^_^')

if __name__ == '__main__':
    file_path = '../dict/en_position_title.dict'

    spell_by_artificail(read_lines(file_path), file_path)
    # spell_by_auto(read_lines(file_path), file_path)


