#coding:utf-8


from sklearn import svm
from sklearn import datasets

clf = svm.SVC()
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)


# 使用 pickle 保存
import pickle

with open("save/clf.pickle", 'wb') as f:
    pickle.dump(clf, f)

with open('save/clf.pickle', 'rb') as f:
    clf2 = pickle.load(f)
    print(clf2.predict(X[0:1]))

# 使用 joblib 保存，读取速度更快
from sklearn.externals import joblib
joblib.dump(clf, 'save/clf.pkl')
#读取model
clf3 = joblib.load('save/clf.pkl')
print(clf3.predict(X[0:1]))
