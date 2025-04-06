# API 文档

## GET /search

### 描述
根据查询参数搜索相关记录，并返回分页结果。

### 请求参数
- query (string): 查询关键字
- page (integer, optional): 当前页码，默认为1

### 响应数据
- docs (array): 匹配的记录列表
- length (integer): 总记录数
- value (string): 查询关键字
- spend (float): 搜索耗时

### 示例
```

GET /search?query=example&page=2&filters={"nation":["美国","英国"]} HTTP/1.1
Host: localhost:8080
```
响应：
```
json
{
    "docs": [
        {
            "tech_id": "1",
            "teacher": "张三",
            "major": "计算机科学",
            "school_name": "清华大学"
        },
        ...
    ],
    "length": 100,
    "value": "example",
    "spend": 0.05
}
```
## GET /detail

### 描述
根据 ID 获取详细信息。

### 请求参数
- id (string): 记录ID

### 响应数据
- userlist (object): 匹配的记录详情, 包括"teacher", "major", "school_name"和"introduction"字段。

### 示例
```

GET /detail?id=1 HTTP/1.1
Host: localhost:8080
```
响应：
```
json
{
    "userlist": {
        "teacher": "张三",
        "major": "计算机科学",
        "school_name": "清华大学",
        "introduction": "张三是一个计算机科学专业的老师，他喜欢研究计算机技术。"
    }
}
