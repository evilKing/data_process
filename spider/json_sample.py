#coding:utf-8


import json

str = '''
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''

print(type(str))
data = json.loads(str)
print(data)
print(type(data))
print(data[0]['name'])
print(data[0].get('name2', 'gay'))


with open('data.json', 'r') as file:
	str = file.read()
	data = json.loads(str)
	print(data)

data = [{
	'name': 'Bob',
	'gender': 'male',
	'birthday': '1992-10-18'
}]
with open('data.json', 'w') as file:
	file.write(json.dumps(data, indent=2))

data = [{
	'name': '王伟',
	'gender': '男',
	'birthday': '1992-10-18'
}]
with open('data.json', 'w') as file:
	file.write(json.dumps(data, indent=2))

# 为了输出中文，需要指定 ensure_ascii 为 False
# 还要规定文件输出的编码
with open('data.json', 'w', encoding='utf-8') as file:
	file.write(json.dumps(data, indent=2, ensure_ascii=False))
	


