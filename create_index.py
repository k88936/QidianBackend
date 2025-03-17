import os
import json5  # 修改: 使用 json5 库
import pymysql
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NGRAM, ID
from jieba.analyse import ChineseAnalyzer
from db_config import DB_CONFIG  # 导入数据库配置

analyzer = ChineseAnalyzer()
schema = Schema(tech_id=TEXT(stored=True),
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

# createUserSql = '''CREATE TABLE tech_info
#            (
#            TechID                 INT   PRIMARY KEY,
#            school                 VARCHAR(100)   ,
#            department                VARCHAR(100)  ,
#            teacher                 VARCHAR(100)   ,
#            introduction                TEXT,
#            fields                          TEXT,
#            email                    VARCHAR(999),
#            page                     VARCHAR(999)
#            )
# '''
# sql_insert = 'insert into tech_info (TechID,school, department,teacher,introduction,fields,email,page) values {}'
try:
    my_connection = pymysql.connect(**DB_CONFIG)  # 使用配置文件中的配置
    cursor = my_connection.cursor()

except Exception as e:
    print("\033[91mMysql link fail：%s\033[0m" % e)  # 修改: 红色打印
    exit(1)

cursor.execute("select TechID,school,department,teacher,fields from tech_info")
for row in cursor.fetchall():
    url, school_name, department_name, person_name, fields = row
    print("record: school",school_name)
    print("        department",department_name)
    print("        fields:",fields)
    info = school_name +' '+department_name+ ' '+fields.replace('#', '')
    write.add_document(tech_id=url,
                       # school=school_name,
                       # department=department_name,
                       # teacher=person_name,
                       # introduction=person['introduction']
                       info=info
                       )
my_connection.commit()
cursor.close()
my_connection.close()
write.commit()
