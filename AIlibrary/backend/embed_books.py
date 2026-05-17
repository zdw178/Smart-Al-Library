import json
import os
import jieba

def jieba_tokenize(text):
    """使用 jieba 进行中文分词"""
    words = jieba.cut(text, cut_all=False)
    return ' '.join(words)

with open('mock_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

index = []
for book in books:
    tags_str = " ".join(book.get('tags', []))
    emotion = book.get('emotion', '')
    scenario = book.get('scenario', '')
    
    text = f"{book['title']} {book['author']} {book['description']} {tags_str} {emotion} {scenario}"
    
    tokenized_text = jieba_tokenize(text)
    
    index.append({
        'isbn': book['isbn'],
        'title': book['title'],
        'author': book['author'],
        'description': book['description'],
        'rating': book['rating'],
        'call_number': book['call_number'],
        'status': book['status'],
        'tags': book.get('tags', []),
        'emotion': book.get('emotion', ''),
        'scenario': book.get('scenario', ''),
        'tokenized_text': tokenized_text
    })

with open('book_index.json', 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"成功创建图书索引，包含{len(books)}本书")
print(f"示例分词结果: {index[0]['title']} -> {index[0]['tokenized_text'][:50]}...")
