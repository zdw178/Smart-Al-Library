from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import re
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from openai import OpenAI
import jieba

load_dotenv()

app = FastAPI()

deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def jieba_tokenize(text):
    """使用 jieba 进行中文分词，作为 TF-IDF 的自定义分词器"""
    words = jieba.cut(text, cut_all=False)
    return list(words)

with open('mock_data.json', 'r', encoding='utf-8') as f:
    local_books = json.load(f)

corpus = []
for book in local_books:
    tags_str = " ".join(book.get('tags', []))
    emotion = book.get('emotion', '')
    scenario = book.get('scenario', '')
    text = f"{book['title']} {book['author']} {book['description']} {tags_str} {emotion} {scenario}"
    corpus.append(text)

vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize)
tfidf_matrix = vectorizer.fit_transform(corpus)

def rewrite_query_with_llm(query: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("[DeepSeek] No API key found")
        return query
    
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个智能搜索助手。用户输入的搜索词可能包含拼音、错别字或模糊意图。请将其纠正、提炼为清晰的搜索词（1-3个词组为佳）。你必须只返回纠正后的词语，严禁输出任何额外解释或标点符号！"
                },
                {
                    "role": "user",
                    "content": f"纠正这个搜索词：{query}"
                }
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        content = response.choices[0].message.content.strip()
        content = content.replace("'", "").replace('"', '').replace('.', '').replace('。', '')
        
        if content:
            print(f"[Query Rewrite] 原始: {query} -> 重写后: {content}")
            return content
            
    except Exception as e:
        print(f"DeepSeek 重写查询失败: {e}")
    
    return query

def get_similar_books(book_idx, top_k=2):
    book_vec = tfidf_matrix[book_idx]
    sims = cosine_similarity(book_vec, tfidf_matrix).flatten()
    sorted_indices = np.argsort(sims)[::-1]
    
    similar = []
    for idx in sorted_indices:
        if idx == book_idx:
            continue
        b = local_books[idx]
        similar.append({
            "title": b["title"],
            "rating": b["rating"],
            "emotion": b.get("emotion", "")
        })
        if len(similar) >= top_k:
            break
    return similar

def clean_json_string(content: str) -> str:
    """清理 JSON 字符串，移除 Markdown 标记"""
    if not content:
        return content
    
    content = content.strip()
    
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    
    if content.endswith("```"):
        content = content[:-3]
    
    content = content.strip()
    
    return content

def generate_recommendation_with_deepseek(query: str, books: list) -> dict:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("[DeepSeek] No API key found")
        return {
            "recommendation": f"系统基于您查询的「{query}」，为您匹配了以下书籍。",
            "tags": []
        }
    
    books_context = "\n".join([
        f"- 《{book.get('title', '')}》 作者：{book.get('author', '')} 评分：{book.get('rating', '')}"
        for book in books
    ])
    
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个专业的图书馆AI助手。你需要根据用户的查询和推荐书籍列表，生成一段推荐理由。

请以JSON格式返回，结构如下：
{
    "recommendation": "推荐理由（2-3句话，解释为什么这些书适合用户）",
    "tags": ["标签1", "标签2", "标签3"]（与查询相关的3-5个标签）
}

注意：
1. 推荐理由要简洁、有说服力，突出书籍的特色
2. 标签要与查询和书籍内容相关
3. 只返回JSON，不要有其他文字"""
                },
                {
                    "role": "user",
                    "content": f"""用户查询：「{query}」

推荐书籍列表：
{books_context}

请根据以上信息生成推荐理由和标签。"""
                }
            ],
            temperature=0.7,
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        print(f"[DeepSeek Recommendation] Raw response: {content}")
        
        cleaned_content = clean_json_string(content)
        print(f"[DeepSeek Recommendation] Cleaned response: {cleaned_content}")
        
        result = json.loads(cleaned_content)
        print(f"[DeepSeek Recommendation] Parsed result: {result}")
        return result
        
    except json.JSONDecodeError as e:
        print(f"[DeepSeek ERROR] JSON 解析失败! Raw content: {content}")
        print(f"[DeepSeek ERROR] Error detail: {e}")
        return {
            "recommendation": f"系统基于您查询的「{query}」，为您匹配了以下书籍。",
            "tags": []
        }
    except Exception as e:
        print(f"[DeepSeek ERROR] 生成推荐失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "recommendation": f"系统基于您查询的「{query}」，为您匹配了以下书籍。",
            "tags": []
        }

def gemini_web_search(query: str) -> str:
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    if not gemini_api_key:
        print("[Gemini] No API key found")
        return ""
    
    print(f"[Gemini] Starting web search for: {query}")
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-lite:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    
    sys_prompt = "你是一个专业的图书信息搜索助手。请根据用户查询，搜索最新、最准确的相关信息。返回内容要简洁明了，突出重点信息。"
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": f"{sys_prompt}\n\n请搜索以下图书相关信息：{query}\n\n请提供：\n1. 图书基本信息（作者、出版社、出版时间）\n2. 内容简介\n3. 相关推荐\n4. 最新评价\n\n返回中文，保持信息准确。"
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1000
        }
    }
    
    try:
        print(f"[Gemini] Sending request to: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"[Gemini] Response status code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            print(f"[Gemini Web Search] 查询: {query} -> 结果: {content[:100]}...")
            return content
        else:
            print(f"[Gemini] Error response: {response.text}")
    except Exception as e:
        print(f"[Gemini] 联网搜索失败: {e}")
        import traceback
        traceback.print_exc()
    
    return ""

@app.get("/")
def read_root():
    return {"message": "SmartLib AI Backend is Running with RAG Vector Search + Jieba"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "books_count": len(local_books)}

@app.get("/api/search/exact")
def exact_search(query: str = Query(..., description="搜索关键词")):
    results = []
    for book in local_books:
        if (query.lower() in book['title'].lower() or
            query.lower() in book['author'].lower()):
            results.append(book)
    return {"results": results, "count": len(results)}

@app.get("/api/search/smart")
def smart_search(query: str = Query(..., description="自然语言搜索关键词")):
    print(f"\n[Smart Search] =======================================")
    print(f"[Smart Search] Received query: {query}")
    
    rewritten_query = rewrite_query_with_llm(query)
    print(f"[Smart Search] Rewritten query: {rewritten_query}")
    
    print("[Smart Search] Step 2: Vectorizing query with Jieba")
    query_vec = vectorizer.transform([rewritten_query])
    
    print("[Smart Search] Step 3: Calculating cosine similarity")
    sims = cosine_similarity(query_vec, tfidf_matrix).flatten()
    print(f"[Smart Search] Similarity scores: {sims}")
    
    top_indices = np.argsort(sims)[::-1][:4]
    print(f"[Smart Search] Top indices: {top_indices}")
    
    results = []
    for idx in top_indices:
        book_obj = dict(local_books[idx])
        book_obj["similar_books"] = get_similar_books(idx, top_k=2)
        book_obj["similarity_score"] = float(sims[idx])
        results.append(book_obj)
        print(f"[Search Debug] Match: {book_obj['title']} (Score: {sims[idx]:.4f})")
            
    if not results:
        print("[Smart Search] No results found, using default recommendations")
        results = [dict(local_books[0]), dict(local_books[1]), dict(local_books[2])]
        for r in results:
            idx = local_books.index(next(b for b in local_books if b["isbn"] == r["isbn"]))
            r["similar_books"] = get_similar_books(idx, top_k=2)

    print("\n[Smart Search] === Top-3 本地检索结果 ===")
    for i, book in enumerate(results[:3], 1):
        print(f"  {i}. 《{book['title']}》 - 作者: {book['author']} (相似度: {book.get('similarity_score', 'N/A'):.4f})")
    print("[Smart Search] =============================\n")
    
    print("[Smart Search] Step 5: Generating recommendation with DeepSeek")
    deepseek_result = generate_recommendation_with_deepseek(rewritten_query, results[:3])
    
    print("[Smart Search] Step 6: Performing web search with Gemini")
    web_search_result = gemini_web_search(rewritten_query)
    print(f"[Smart Search] Web search result length: {len(web_search_result)}")

    print("[Smart Search] Step 7: Returning response")
    return {
        "results": results[:3],
        "count": min(len(results), 3),
        "rewritten_query": rewritten_query,
        "web_search": web_search_result,
        "recommendation": deepseek_result.get("recommendation", f"系统基于您查询的「{rewritten_query}」，为您匹配了以下书籍。"),
        "tags": deepseek_result.get("tags", [])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
