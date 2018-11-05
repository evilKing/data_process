#coding:utf8

import re
import multiprocessing
import signal

from signal_regex.resume_xhtml_repr import html_repr

data_root = '/Users/hulk/Workspace/PycharmProjects/data_process/dict'

def time_out(b, c):
    raise TimeoutError

def search_with_timeout(pipe, word, value):
    signal.signal(signal.SIGALRM, time_out)
    signal.alarm(1)
    r = re.compile(word)
    try:
        ret = r.search(value, re.I)
        b_ret = True if ret != None else False
        pipe.send(b_ret)
    except TimeoutError:
        pipe.send(False)

fr = open(data_root + '/docx2html4.html')
lines = fr.readlines()
fr.close()

lines = map(lambda x: x.strip(), lines)
for line in lines:
    print(line)
for line in html_repr.parse_cont_lines(lines) :
    print(line)

# pipe = multiprocessing.Pipe()
# p = multiprocessing.Process(target = search_with_timeout, args = (pipe[0], word, left_value))
# p.start()
# p.join() #等待进程的结束
# ret =  pipe[1].recv() #获取管道中的数据



