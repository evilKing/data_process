#coding:utf-8

from sklearn import linear_model

reg = linear_model.LinearRegression()
reg.fit([[0,0],[1,1],[2,2]], [0,1,2])
print(reg.coef_)
print(reg.intercept_)

# 岭回归
from sklearn import linear_model
reg = linear_model.Ridge(alpha=0.5)
reg.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
print(reg.coef_)
print(reg.intercept_)

# 广义交叉验证
reg = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
reg.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
print(reg.coef_)
print(reg.alpha_)

# Lasso 估计稀疏系数的线性模型
reg = linear_model.Lasso(alpha=0.1)
reg.fit([[0, 0], [1, 1]], [0, 1])
print(reg.predict([[1,1]]))

# 多项式回归

from sklearn.preprocessing import PolynomialFeatures
import numpy as np

X = np.arange(6).reshape(3, 2)
print(X)
poly = PolynomialFeatures(degree=2)
poly.fit_transform(X)

# 借助 Pipeline 工具进行简化
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

model = Pipeline([('poly', PolynomialFeatures(degree=3)),
                  ('linear', LinearRegression(fit_intercept=False))])
x = np.arange(5)
y = 3 - 2*x + x ** 2 -x ** 3
model = model.fit(x[:, np.newaxis], y)
print(model.named_steps['linear'].coef_)






