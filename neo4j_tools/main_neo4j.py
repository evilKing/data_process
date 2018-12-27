#coding:utf-8


from py2neo import Graph, Node, Relationship

graph = Graph('http://localhost:7474', username='neo4j', password='evilking')

graph.delete_all()

test_node_1 = Node(label='ru_yi_zhuan', name='皇帝')
test_node_2 = Node(label='ru_yi_zhuan', name='皇后')
test_node_3 = Node(label='ru_yi_zhuan', name='公主')
graph.create(test_node_1)
graph.create(test_node_2)
graph.create(test_node_3)

node_1_zhangfu_node_1 = Relationship(test_node_1, '丈夫', test_node_2)
node_1_zhangfu_node_1['count'] = 1
node_2_qizi_node_1 = Relationship(test_node_2, '妻子', test_node_1)
node_2_munv_node_1 = Relationship(test_node_2, '母女', test_node_3)

node_2_qizi_node_1['count'] = 1

graph.create(node_1_zhangfu_node_1)
graph.create(node_2_qizi_node_1)
graph.create(node_2_munv_node_1)

print(graph)
print(test_node_1)
print(test_node_2)
print(node_1_zhangfu_node_1)
print(node_2_qizi_node_1)
print(node_2_munv_node_1)



a = Node('Person', name='Alice')
b = Node('Person', name='Bob')
r = Relationship(a, 'KNOWS', b)

print(a, b, r)
a['age'] = 20
b['age'] = 21
r['time'] = '2017/08/31'
a.setdefault('location', '北京')
print(a, b, r)

data = {
    'name': 'Amy',
    'age': 21
}
a.update(data)
print(a)

# 子图
s1 = a | b | r
s2 = a | b
print(s1 & s2)
graph.create(s1)

print(s1.keys())
print(s1.labels)
print(s1.nodes)
print(s1.relationships)
print(s1.types())

# 遍历
from py2neo import walk

c = Node('Person', name='Mike')
ab = Relationship(a, 'KNOWS', b)
ac = Relationship(a, 'KNOWS', c)
w = ab + Relationship(b, 'LIKES', c) + ac
for item in walk(w):
    print(item)

data = graph.evaluate('MATCH (p:Person) return p')
print(data)
from pandas import DataFrame
# df = DataFrame(data)
# print(df)

a = Node('Person', name='alice2')
relationship = graph.match_one(r_type='KNOWS')
print(relationship)
# node = graph.find_one(label='Person')
# print(node)
graph.delete(relationship)

relationship = graph.match_one(r_type='KNOWS')
print(relationship)



