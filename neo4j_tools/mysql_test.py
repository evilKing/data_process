#coding:utf-8

import pymysql

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'evilking',
    'charset': 'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
}
conn = pymysql.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()

try:
    DB_NAME = 'test'
    cursor.execute('drop database if exists %s' % DB_NAME)
    cursor.execute('create database if not exists %s' % DB_NAME)
    conn.select_db(DB_NAME)

    TABLE_NAME = 'user'
    cursor.execute('create table %s (id int primary key, name varchar(30))' % TABLE_NAME)

    values = []
    for i in range(20):
        values.append((i, 'kk' + str(i)))
    cursor.executemany('insert into user values(%s, %s)', values)

    count = cursor.execute('select * from %s' % TABLE_NAME)
    print('total records:', cursor.rowcount)

    desc = cursor.description
    print('%s %3s' % (desc[0][0], desc[1][0]))

    cursor.scroll(10, mode='absolute')
    results = cursor.fetchall()
    for result in results:
        print(result)

except:
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    cursor.close()
    conn.close()


