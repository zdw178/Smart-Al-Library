import requests

# 测试智能搜索接口
query = "人工智能"
url = f"http://localhost:8001/api/search/smart?query={query}"

print(f"Testing smart search with query: {query}")
print(f"URL: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"Status code: {response.status_code}")
    data = response.json()
    print(f"Results count: {data.get('count')}")
    print("Results:")
    for book in data.get('results', []):
        print(f"  - {book.get('title')} by {book.get('author')}")
    print(f"Web search result: {data.get('web_search', '')[:100]}...")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()