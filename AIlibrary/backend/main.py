from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
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

def search_real_books_with_deepseek(query: str) -> list:
    """使用 DeepSeek 的知识库搜索真实存在的图书，返回结构化数据"""
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("[DeepSeek Search] No API key found")
        return []

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个专业的图书搜索助手。根据用户的搜索查询，从你的知识库中推荐最相关的真实存在的图书。

你必须以严格的JSON格式返回，结构如下：
{
    "books": [
        {
            "title": "真实存在的书名",
            "author": "真实作者名",
            "description": "真实内容简介（80-150字）",
            "rating": "豆瓣评分（如8.5，若不确定填''）",
            "tags": ["标签1", "标签2", "标签3"],
            "isbn": "ISBN号（如不确定填''）"
        }
    ]
}

要求：
1. 只返回真实存在的图书，严禁编造
2. 返回3-5本最相关的图书
3. 描述要准确反映图书内容
4. 标签要与图书主题相关
5. 只返回JSON，不要其他任何文字"""
                },
                {
                    "role": "user",
                    "content": f"请搜索与以下查询最相关的真实图书：{query}"
                }
            ],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()
        content = clean_json_string(content)
        result = json.loads(content)
        books = result.get("books", [])

        # 为每本书补充 BookCard 渲染所需的字段
        for i, book in enumerate(books):
            book.setdefault("isbn", "")
            book.setdefault("call_number", f"I{book.get('author', '')[:2]}/{i+1}")
            book.setdefault("status", "在馆")
            book.setdefault("emotion", book.get("tags", ["推荐"])[0] if book.get("tags") else "推荐")
            book.setdefault("scenario", "")
            book.setdefault("similarity_score", 1.0)
            book.setdefault("similar_books", [])
            book["source"] = "deepseek"

        # 为真实图书之间建立相似推荐关系
        for i, book in enumerate(books):
            if not book.get("similar_books"):
                sims = []
                for j, other in enumerate(books):
                    if i != j:
                        sims.append({
                            "title": other.get("title", ""),
                            "rating": other.get("rating", ""),
                            "emotion": other.get("emotion", "")
                        })
                book["similar_books"] = sims[:2]

        print(f"[DeepSeek Search] 查询: {query} -> 找到 {len(books)} 本真实图书")
        for b in books:
            print(f"  - 《{b.get('title', '')}》 {b.get('author', '')} (评分: {b.get('rating', 'N/A')})")
        return books

    except json.JSONDecodeError as e:
        print(f"[DeepSeek Search] JSON解析失败: {e}")
        print(f"[DeepSeek Search] Raw content: {content}")
        return []
    except Exception as e:
        print(f"[DeepSeek Search] 搜索失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def merge_book_results(real_books: list, mock_books: list, max_results: int = 5) -> list:
    """合并真实图书和模拟数据，去重，真实结果优先"""
    merged = []
    seen_titles = set()

    for book in real_books:
        title_key = book.get("title", "").strip().lower()
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            merged.append(book)

    for book in mock_books:
        title_key = book.get("title", "").strip().lower()
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            merged.append(book)

    print(f"[Merge] 真实图书: {len(real_books)}本, Mock: {len(mock_books)}本, 合并后: {len(merged)}本")
    return merged[:max_results]

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

@app.get("/api/discovery")
def discovery():
    """快速发现端点 - 不调用任何 LLM，直接返回高分书籍"""
    sorted_books = sorted(local_books, key=lambda b: float(b.get('rating', 0)), reverse=True)
    return {"results": sorted_books[:3], "count": 3}

@app.get("/api/search/exact")
def exact_search(query: str = Query(..., description="搜索关键词")):
    results = []
    for book in local_books:
        if (query.lower() in book['title'].lower() or
            query.lower() in book['author'].lower()):
            results.append(book)
    return {"results": results, "count": len(results)}

@app.get("/api/search/smart")
async def smart_search(query: str = Query(..., description="自然语言搜索关键词")):
    print(f"\n[Smart Search] =======================================")
    print(f"[Smart Search] Received query: {query}")

    # Step 1: 并行 — 查询改写 + DeepSeek 真实图书搜索
    print("[Smart Search] Step 1: Query rewrite + Real book search (parallel)")
    rewritten_query, real_books = await asyncio.gather(
        asyncio.to_thread(rewrite_query_with_llm, query),
        asyncio.to_thread(search_real_books_with_deepseek, query)
    )
    print(f"[Smart Search] Rewritten query: {rewritten_query}")
    print(f"[Smart Search] Real books found: {len(real_books)}")

    # Step 2: TF-IDF Mock数据搜索（兜底 + 补充）
    print("[Smart Search] Step 2: TF-IDF mock data search")
    query_vec = vectorizer.transform([rewritten_query])
    sims = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = np.argsort(sims)[::-1][:4]

    mock_results = []
    for idx in top_indices:
        book_obj = dict(local_books[idx])
        book_obj["similar_books"] = get_similar_books(idx, top_k=2)
        book_obj["similarity_score"] = float(sims[idx])
        book_obj["source"] = "mock"
        mock_results.append(book_obj)

    # Step 3: 合并结果 — 真实图书优先
    merged_results = merge_book_results(real_books, mock_results)

    if not merged_results:
        print("[Smart Search] No results, using mock defaults")
        merged_results = [dict(local_books[0]), dict(local_books[1]), dict(local_books[2])]
        for r in merged_results:
            r["source"] = "mock"
            r.setdefault("similar_books", [])
            r.setdefault("similarity_score", 0.0)

    print("\n[Smart Search] === Final Results ===")
    for i, book in enumerate(merged_results, 1):
        print(f"  {i}. 《{book.get('title', '')}》 {book.get('author', '')} (来源: {book.get('source', '')})")
    print("[Smart Search] ======================\n")

    # Step 4: 并行 — 推荐生成 + Gemini 联网搜索
    print("[Smart Search] Step 4: Recommendation + Gemini search (parallel)")
    deepseek_result, web_search_result = await asyncio.gather(
        asyncio.to_thread(generate_recommendation_with_deepseek, rewritten_query, merged_results[:3]),
        asyncio.to_thread(gemini_web_search, rewritten_query)
    )

    return {
        "results": merged_results[:3],
        "count": len(merged_results[:3]),
        "rewritten_query": rewritten_query,
        "web_search": web_search_result,
        "recommendation": deepseek_result.get("recommendation", f"系统基于您查询的「{rewritten_query}」，为您匹配了以下书籍。"),
        "tags": deepseek_result.get("tags", [])
    }

print(f"[Startup] CWD: {os.getcwd()}")
print(f"[Startup] __file__: {__file__}")
print(f"[Startup] Books loaded: {len(local_books)}")
print(f"[Startup] DeepSeek API Key: {'configured' if os.getenv('DEEPSEEK_API_KEY') else 'MISSING'}")

# 托管前端静态文件（生产环境用）
# __file__ 是 main.py 的绝对路径，所以相对路径基于 backend/ 目录
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
frontend_dist = os.path.abspath(frontend_dist)
print(f"[Startup] Frontend dist path: {frontend_dist}")
print(f"[Startup] Dist exists: {os.path.exists(frontend_dist)}")
if os.path.exists(frontend_dist):
    try:
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
        print("[Startup] Frontend static files mounted successfully")
    except Exception as e:
        print(f"[Startup] Failed to mount frontend: {e}")
else:
    print("[Startup] WARNING: frontend/dist not found, only API routes available")
    # 确保 API 路由不被影响
    @app.get("/")
    def root_fallback():
        return {"message": "SmartLib API is running. Frontend not deployed."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
