# -*- coding: utf-8 -*-
"""
@author: Administrator
"""
import os
import json5  # 修改: 使用 json5 库
import pymysql
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NGRAM, ID
from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()
schema = Schema(tech_id=ID(stored=True, analyzer=analyzer),
                # department=TEXT(stored=True, analyzer=analyzer),
                # school=TEXT(stored=True, analyzer=analyzer),
                # teacher=TEXT(stored=True),
                # introduction=TEXT(stored=True, analyzer=analyzer),
                info=TEXT(stored=True, analyzer=analyzer),
                )

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)
write = ix.writer()

# --------------------------------------------------------------------------
# 读取本地的data.json文件  在数据库中建一个tech_info表   将data.json内容插入到数据库中
# --------------------------------------------------------------------------
path = './data/data.json5'
with open(path, 'r', encoding='utf-8') as file:
    content = file.read()
    # 清理不可见字符
    data = json5.loads(content)  # 修改: 使用 json5.loads 方法
createUserSql = '''CREATE TABLE tech_info         
           (
           TechID                 INT   PRIMARY KEY,
           school                 VARCHAR(100)   ,
           department                VARCHAR(100)  , 
           teacher                 VARCHAR(100)   ,
           introduction                TEXT, 
           fields                          TEXT,
           email                    VARCHAR(999),
           page                     VARCHAR(999)
           )
'''
sql_insert = 'insert into tech_info (TechID,school, department,teacher,introduction,fields,email,page) values {}'
uuid = 1  # 修改: uuid 从 1 开始
print("start")
try:
    my_connection = pymysql.connect(user="root",
                                    password="root",
                                    port=3306,
                                    host="127.0.0.1",  # 本地数据库  等同于localhost
                                    db="school",
                                    charset="utf8")
    cursor = my_connection.cursor()

except Exception as e:
    print("\033[91mMysql link fail：%s\033[0m" % e)  # 修改: 红色打印
    exit(1)
try:
    cursor.execute("drop table if exists tech_info")
    cursor.execute(createUserSql)
except Exception as e:
    print("\033[91mdont do created table sql: %s\033[0m" % e)  # 修改: 红色打印

for school in data:
    school_name = school['name']
    print(">>> school_name:", school_name)
    if 'each_department' not in school:
        continue
    departments = school['each_department']
    for department in departments:
        department_name = department['name']
        print(">>> >>> department_name:", department_name)
        if 'people' not in department:
            continue
        people = department['people']
        for person in people:
            person_name = person['name']
            print(">>> >>> >>> person_name:", person_name)
            if 'introduction' not in person:
                continue
            if 'info' not in person:
                continue
            if 'research-direction' not in person['info']:
                continue

            research_direction = person['info']['research-direction']
            if isinstance(research_direction, list):
                research_direction_str = '#'.join(research_direction)
            else:
                research_direction_str = research_direction
            email_addr = person['info']['email'] if 'email' in person['info'] else ''
            page_addr = person['info']['page'] if 'page' in person['info'] else person['url']

            x = [uuid, school_name, department_name, person_name, person['introduction'], research_direction_str,
                 email_addr, page_addr]
            print("           ====")
            print('           ', person)
            print("           *****")
            sql = sql_insert.format(tuple(x))
            print('           ', sql)
            try:
                cursor.execute(sql)
            except Exception as e:
                print("\033[91mMysql insert fail: %s\033[0m" % e)  # 修改: 红色打印
                my_connection.rollback()
                exit(2)
            try:
                info = '#'.join([school_name, department_name, person_name, research_direction_str])
                print(info)
                write.add_document(tech_id=str(uuid),
                                   # school=school_name,
                                   # department=department_name,
                                   # teacher=person_name,
                                   # introduction=person['introduction']
                                   info=info
                                   )
            except Exception as e:
                print("\033[91mWhoosh insert fail: %s\033[0m" % e)  # 修改: 红色打印
                exit(1)
            uuid += 1  # 修改: uuid 自增放在正确的位置

my_connection.commit()
cursor.close()
my_connection.close()
write.commit()
