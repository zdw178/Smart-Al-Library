import json
import random
import uuid

# 构建书名与作者的语料库
categories = {
    "技术类": {
        "titles": ["{}底层架构", "{}实战开发指南", "深入理解{}", "{}权威指南", "{}：从入门到放弃"],
        "keywords": ["单片机", "大模型", "Python", "机器视觉", "控制工程", "自动化", "嵌入式", "PCB设计"],
        "tags": ["极客", "硬核编程", "考研冲刺", "期末复习"],
        "emotion": "烧脑",
        "scenario": "专业课攻坚, 实验室打卡"
    },
    "经管类": {
        "titles": ["{}的逻辑", "{}：商业新物种", "宏观{}", "{}原理与应用", "硅谷{}指南"],
        "keywords": ["商业模式", "经济学", "管理学", "财务报表", "市场营销", "案例分析", "创业", "组织行为"],
        "tags": ["搞钱搞事业", "认知升级", "商业思维", "经管必读"],
        "emotion": "充满干劲",
        "scenario": "路演准备, 职场进阶"
    },
    "文学小说": {
        "titles": ["{}的秘密", "消失的{}", "{}的救赎", "{}历险记", "最后一个{}"],
        "keywords": ["宇宙", "帝国", "杂货铺", "嫌疑人", "风之影", "基地", "森林", "黑客"],
        "tags": ["治愈系", "烧脑推理", "赛博朋克", "经典文学"],
        "emotion": "沉浸治愈",
        "scenario": "睡前读物, 周末放松"
    }
}

surnames = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", "理查德", "托马斯", "艾伦"]
names = ["伟", "芳", "娜", "强", "军", "洋", "勇", "大卫", "阿西莫夫", "图灵"]

books = []

for i in range(1000):
    # 随机选一个类别
    cat_name = random.choice(list(categories.keys()))
    cat_data = categories[cat_name]
    
    # 组合书名和作者
    title_template = random.choice(cat_data["titles"])
    keyword = random.choice(cat_data["keywords"])
    title = title_template.format(keyword)
    author = random.choice(surnames) + random.choice(names)
    
    # 生成其他随机属性
    isbn = "9787" + str(random.randint(100000000, 999999999))
    rating = round(random.uniform(7.0, 9.8), 1)
    call_number = f"{random.choice(['TP', 'F', 'I', 'O'])}{random.randint(100, 999)}/{random.randint(10, 99)}"
    status = random.choice(["在馆", "在馆", "借出"]) # 增加在馆的概率
    
    # 随机抽取 2-3 个标签
    tags = random.sample(cat_data["tags"] + [keyword], k=random.randint(2, 3))
    
    book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "description": f"这是一本关于{keyword}的经典著作，深度剖析了相关领域的底层逻辑与实战应用，广受好评。",
        "rating": rating,
        "call_number": call_number,
        "status": status,
        "tags": tags,
        "emotion": cat_data["emotion"],
        "scenario": cat_data["scenario"]
    }
    books.append(book)

# 写入 JSON 文件
with open("mock_data.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f"🎉 成功！1000本模拟图书数据已写入 mock_data.json！")
print(f"⚠️ 注意：请务必重新运行 python embed_books.py 更新向量数据库！")