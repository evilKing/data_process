# coding: utf-8
import os, re
import chardet
import sys
import jieba

split_pat = re.compile('[。！；？，]')

lines = []
def rename_dir(dir):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isdir(file_path):
            rename_dir(file_path)
        else:
            print(file_path)
            with open(file_path, 'rb') as fr:
                try:
                    for line in fr:
                        line = line.decode('GB2312')
                        if line.strip() == '':
                            continue
                        for sent in split_pat.split(line):
                            words = list(jieba.cut(sent))
                            lines.append(' '.join(words))
                except:
                    pass

def write_lines(lines):
    fw = open('cn_noval.txt', 'w')
    fw.writelines(lines)
    fw.flush()
    fw.close()


if __name__ == '__main__':
    path = '/Users/hulk/Document/baidu_disk/Novel/'
    rename_dir(path)
    write_lines(lines)