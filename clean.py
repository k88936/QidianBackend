import json5
import re

path = './data/data.json5'
with open(path, 'r', encoding='utf-8') as file:
    content = file.read()
# 使用正则表达式合并两次替换
content = re.sub(r'[\u2028\u2029]', '', content)
# content = content.replace('\n', '')
# content = content.replace('\\', '')
data = json5.loads(content)
# 写回文件
with open(path, 'w', encoding='utf-8') as file:
    json5.dump(data, file, ensure_ascii=False, indent=4)