#coding:utf-8


def func1(val):
    lista = []
    for i in range(val):
        lista.append(i)

    return lista

def my_main_test():
    val = 'abcdefghijk'
    val_list = list(val)
    for j in range(len(val_list)):
        # if j % 2 == 0:
        #     del val_list[j]
        # print(j, 'main_test', str(val_list), len(val_list))
        pass

    print("==========")

if __name__ == '__main__':
    my_main_test()
