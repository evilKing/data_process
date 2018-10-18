#coding:utf-8

import dis


class A:
    def test(self):
        pass

    def test2(self):
        print('aaaa')

# dis.dis(A)

c = compile('1+2', 'test.py', 'single')
dis.dis(c)

