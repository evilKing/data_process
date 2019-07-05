#coding:utf-8
import math
import matplotlib.pyplot as plt
import numpy as np

left_info_gain = [3.864570128428202, 3.114910233443627, 2.8122018592852838, 2.6881902982591717, 2.6337090485002106, 2.615566051029563, 2.59698076111882, 2.5933400185415225, 2.592448297324913, 2.591768739897608, 2.5921588640006803, 2.5900659543052917]

x = list(range(1, len(left_info_gain) + 1))
x = [-1 * idx for idx in x]

x = np.array(x)
y = np.array(left_info_gain)
z1 = np.polyfit(x, y, 5)
p1 = np.poly1d(z1)
print(p1) #在屏幕上打印拟合多项式
yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('polyfitting')
plt.show()
plt.savefig('p1.png')
