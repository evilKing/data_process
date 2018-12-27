#coding:utf-8

from sklearn import svm

X = [[0, 0], [1,1]]
y = [0,1]
clf = svm.SVC()
clf.fit(X, y)

print(clf.predict([[2, 2]]))

# 支持向量
print(clf.support_vectors_)
# 获得支持向量的索引
print(clf.support_)
# 为每一个类别获得支持向量的数量
print(clf.n_support_)


# SVM 多分类
X = [[0], [1], [2], [3]]
Y = [0, 1, 2, 3]
clf = svm.SVC(decision_function_shape='ovo')
clf.fit(X, Y)

dec = clf.decision_function([[1]])
print(dec.shape[1])
clf.decision_function_shape = 'ovr'
dec = clf.decision_function([[1]])
print(dec.shape[1])


# 线性 SVM
lin_clf = svm.LinearSVC()
lin_clf.fit(X, Y)
dec = lin_clf.decision_function([[1]])
print(dec.shape[1])


# SVR 回归
from sklearn import svm
X = [[0, 0], [2, 2]]
y = [0.5, 2.5]
clf = svm.SVR()
clf.fit(X, y)
print(clf.predict([[1, 1]]))


# 核函数
linear_svc = svm.SVC(kernel='linear')
print(linear_svc.kernel)
rbf_svc = svm.SVC(kernel='rbf')
print(rbf_svc.kernel)

# 自定义核函数
import numpy as np

def my_kernel(X, Y):
    return np.dot(X, Y.T)

clf = svm.SVC(kernel=my_kernel)


# 使用 Gram 矩阵
X = np.array([[0, 0], [1, 1]])
y = [0, 1]
clf = svm.SVC(kernel='precomputed')

gram = np.dot(X, X.T)
clf.fit(gram, y)

print(clf.predict(gram))




