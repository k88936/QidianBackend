# coding:utf-8
import time

from flask import Flask, request, jsonify, redirect, url_for
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from flask import jsonify
from jieba.analyse import ChineseAnalyzer
import pymysql
# 导入CORS库
from flask_cors import CORS
from whoosh.qparser import QueryParser
ix = open_dir("index")
app = Flask(__name__)
# 配置CORS，允许所有来源的请求
CORS(app)

# 封装SQL语句函数
def func(sql, m='r'):
    py = pymysql.connect(host="127.0.0.1", user="root", passwd='root', db='school')
    cursor = py.cursor()
    data = False
    try:
        cursor.execute(sql)
        if m == 'r':
            # 获取列名
            column_names = [desc[0] for desc in cursor.description]
            # 将结果转换为字典列表
            data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        elif m == 'w':
            py.commit()
            data = cursor.rowcount
    except:
        py.rollback()
    py.close()
    return data


@app.route("/search", methods=['GET'])
def search():
    print('>>> search request')
    query = request.args.get('query')  # 获取查询参数query
    print('query=', query)

    # 获取分页参数
    page = int(request.args.get("page", 0))
    per_page_count = 10



    # 在搜索时应用分页
    with ix.searcher() as searcher:# 使用QueryParser来解析查询
        qp = QueryParser("info", ix.schema)
        q = qp.parse(query)
        start_time = time.time()  # 记录开始时间
        docs = searcher.search_page(q, pagelen=per_page_count, pagenum=page)
        end_time = time.time()  # 记录结束时间
        spend = end_time - start_time  # 计算搜索时间
        abstracts = []

        for doc in docs:
            print("whoosh result:",doc)
            tech_id = doc['tech_id']
            sql = "select teacher, department, school,info from tech_info where TechID = " + str(tech_id) + ";"
            ab = func(sql)
            print("dataBase result:",ab)
            if ab:
                temp={'tech_id': tech_id, 'teacher': ab[0]['teacher'], 'department': ab[0]['department'], 'info': ab[0]['info']}
                abstracts.append(temp)
    return jsonify({"docs": abstracts,"count":100, "spend": spend})


@app.route('/detail')
def detail():
    idd = request.args.get('id')
    print(idd)
    sql = "select school,department,teacher,introduction from tech_info where TechID = " + str(idd) + ";"
    print(sql)
    data = func(sql)
    if data:
        data = data[0]  # 取第一个匹配项
    return jsonify({"data": data})


if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
