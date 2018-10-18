#coding:utf-8

from sklearn import svm

X = [[0, 0], [1, 1]]
Y = [0, 1]

clf = svm.SVC()
clf.fit(X, Y)
clf.predict([[2., 2.]])
clf.predict_proba()


