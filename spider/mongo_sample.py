#coding:utf-8

import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

# 指定数据库
db = client['test']
# 指定集合
collection = db['students']

student1 = {
	'id': '20170101',
	'name': 'Jordan',
	'age': 20,
	'gender': 'male'
}
student2 = {
	'id': '20170102',
	'name': 'Hulk',
	'age': 21,
	'gender': 'male'
}
student3 = {
	'id': '20170102',
	'name': 'Hulk',
	'age': 21,
	'gender': 'male'
}

result = collection.insert([student1, student2])
print(result)

# 官方推荐
result = collection.insert_one(student3)
print(result)
print(result.inserted_id)

# result = collection.insert_many([student1, student2])
# print(result)
# print(result.inserted_ids)

result = collection.find_one({'name': 'Jordan'})
print(type(result))
print(result)

from bson.objectid import ObjectId

result = collection.find_one({'_id': ObjectId('5c08d83a3d5f621464dd54e9')})
print(result)

results = collection.find({'age': 20})
print(result)
for result in results:
	print(result)

results = collection.find({'age': {'$gt': 20}})
print(results)

# 计数
count = collection.find().count()
print(count)
count = collection.find({'age': 20}).count()
print(count)

# 排序
results = collection.find().sort('name', pymongo.ASCENDING)
print([result['name'] for result in results])

# 偏移
results = collection.find().sort('name', pymongo.ASCENDING).skip(2)
print([result['name'] for result in results])

# 限制要取的结果个数
results = collection.find().sort('name', pymongo.ASCENDING).skip(2).limit(5)
print([result['name'] for result in results])

# 更新词典，但会删除原先词条的所有字段，然后写入新字段
condition = {'name': 'Hulk'}
student = collection.find_one(condition)
student['age'] = 25
result = collection.update(condition, student)
print(result)

# 更新词典，不会删除其他值，只会更新指定的字段
condition = {'name': 'Hulk'}
student = collection.find_one(condition)
student['age'] = 26
result = collection.update_one(condition, {'$set': student})
print(result)
print(result.matched_count, result.modified_count)


# 删除
result = collection.remove({'name': 'Hulk'})
print(result)

# 推荐，删除第一个匹配
result = collection.delete_one({'name': 'Hulk'})
print(result)
print(result.deleted_count)
# 删除所有匹配
result = collection.delete_many({'age': {'$lt': 25}})
print(result.deleted_count)




