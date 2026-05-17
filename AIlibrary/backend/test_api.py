import requests
import time

# 测试智能搜索API
url = "http://localhost:8001/api/search/smart"
params = {"query": "2026年人工智能最新书籍"}

print("Testing API...")
print(f"URL: {url}")
print(f"Params: {params}")

try:
    start_time = time.time()
    print(f"Sending request...")
    response = requests.get(url, params=params, timeout=60)
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("Response received, parsing JSON...")
        data = response.json()
        print(f"Results count: {data.get('count', 0)}")
        print(f"Rewritten query: {data.get('rewritten_query', 'N/A')}")
        web_search = data.get('web_search', 'N/A')
        print(f"Web search result: {web_search[:200]}...")
        print(f"Recommendation: {data.get('recommendation', 'N/A')[:100]}...")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()