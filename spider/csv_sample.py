#coding:utf-8

import csv

with open('data.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ')
	writer.writerow(['id', 'name', 'age'])
	writer.writerow(['10001', 'Mike', 20])
	writer.writerow(['10002', 'Bob', 22])
	writer.writerow(['10003', 'Jordan', 21])
	# 一次写入多行
	writer.writerows([['10004', 'Hulk', 22], ['10005', 'Bruce', 23], ['10006', 'Leo', 24]])


with open('data.csv', 'w', encoding='utf-8') as csvfile:
	fieldnames = ['id', 'name', 'age']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})
	writer.writerow({'id': '10002', 'name': '王伟', 'age': 22})

with open('data.csv', 'r', encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print(row)

import pandas as pd

df = pd.read_csv('data.csv')
print(df)

