import requests
import urllib.parse

# 测试智能搜索API
query = "人工智能"
encoded_query = urllib.parse.quote(query)
url = f"http://localhost:8001/api/search/smart?query={encoded_query}"

print(f"Testing API with URL: {url}")
try:
    response = requests.get(url, timeout=30)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()