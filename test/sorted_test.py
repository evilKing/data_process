#coding:utf8

def cmp_func(x, y):
    if x[1] < y[1]:
        return -1
    if x[1] > y[1]:
        return 1
    if x[0] < y[0]:
        return -1
    if x[0] > y[0]:
        return 1

    return 0

la = [('a', 1, 'a1'), ('b', 4, 'b4'), ('t', 9, 't9'), ('d', 3, 'd3')]
sorted(la, key=lambda x,y: cmp_func(x,y))
