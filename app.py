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
from db_config import DB_CONFIG  # 导入数据库配置

ix = open_dir("index")
app = Flask(__name__)
# 配置CORS，允许所有来源的请求
CORS(app)


# 封装SQL语句函数
def func(sql, m='r'):
    py = pymysql.connect(**DB_CONFIG)  # 使用配置文件中的配置
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


result_count_limit = 100


@app.route("/search", methods=['GET'])
def search():
    print('>>> search request')
    query = request.args.get('query')  # 获取查询参数query
    print('query=', query)

    # 获取分页参数
    page = int(request.args.get("page", 0))
    per_page_count = 10

    # 获取过滤参数
    filters = request.args.get('filters')
    filter_conditions = None
    if filters:
        filters = eval(filters)  # 将字符串转换为字典
        if 'nation' in filters:
            from whoosh.query import Term, Or
            nations = filters['nation']
            filter_conditions = Or([Term('school_nation', nation) for nation in nations])

    # 在搜索时应用分页
    with ix.searcher() as searcher:
        # 使用QueryParser来解析查询
        qp = QueryParser("info", ix.schema)
        q = qp.parse(query)
        start_time = time.time()  # 记录开始时间

        # 获取总结果数
        docs = searcher.search(q, limit=result_count_limit, filter=filter_conditions)  # 应用过滤器
        total_results = min(len(docs), result_count_limit)

        # 获取分页结果
        # docs = searcher.search_page(q, pagelen=per_page_count, pagenum=page)
        end_time = time.time()  # 记录结束时间
        spend = end_time - start_time  # 计算搜索时间
        abstracts = []
        for doc in docs:
            print("whoosh result:", doc)
            tech_id = doc['tech_id']
            sql = "select teacher, department, school,fields,email,page from tech_info where TechID = " + str(
                tech_id) + ";"
            ab = func(sql)
            print("dataBase result:", ab)
            if ab:
                temp = {
                    "tech_id": tech_id,
                    "teacher": ab[0]['teacher'],
                    "department": ab[0]['department'],
                    # "introduction": ab[0]['introduction'],
                    "school": ab[0]['school'],
                    "fields": ab[0]['fields'],
                    "email": ab[0]['email'],
                    "page": ab[0]['page'],
                    "info": doc['info']
                }
                abstracts.append(temp)
        print("count: ", total_results)
    return jsonify({"docs": abstracts, "spend": spend, "count": total_results})


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
    app.run(host='0.0.0.0', port=5073, debug=False)