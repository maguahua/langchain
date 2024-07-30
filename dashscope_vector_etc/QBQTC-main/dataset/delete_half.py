import json
import random

data = []
with open('train.json', 'r', encoding='utf-8') as file:
    for line in file:
        data.append(json.loads(line))

# 确定要删除的数量
num_to_delete = len(data) // 2

# 随机选择要删除的索引
indices_to_delete = set(random.sample(range(len(data)), num_to_delete))

# 保留未删除的数据
new_data = [item for i, item in enumerate(data) if i not in indices_to_delete]

# 将结果写入新的JSONL文件
with open('new_train.json', 'w', encoding='utf-8') as file:
    for item in new_data:
        file.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"已删除 {num_to_delete} 条数据，并将结果保存到 new_data.json 文件中。")
