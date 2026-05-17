import requests

# 测试智能搜索接口
query = "人工智能"
url = f"http://localhost:8001/api/search/smart?query={query}"

print(f"Testing smart search with query: {query}")
print(f"URL: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# 测试精确搜索接口
print("\nTesting exact search:")
url = f"http://localhost:8001/api/search/exact?query={query}"
try:
    response = requests.get(url, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")