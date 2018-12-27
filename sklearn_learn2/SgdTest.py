#coding:utf-8

from sklearn.linear_model import SGDClassifier

X = [[0, 0], [1, 1]]
y = [0, 1]
clf = SGDClassifier(loss='hinge')
clf.fit(X, y)

print(clf.predict([[2, 2]]))
print(clf.intercept_)

# 使用 log 损失
clf = SGDClassifier(loss='log').fit(X, y)
print(clf.predict_proba([[1, 1]]))




