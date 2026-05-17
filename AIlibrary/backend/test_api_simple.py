import requests

# 测试健康检查接口
print("Testing health check...")
try:
    response = requests.get("http://localhost:8001/health", timeout=10)
    print(f"Health check status: {response.status_code}")
    print(f"Health check response: {response.text}")
except Exception as e:
    print(f"Health check error: {e}")

# 测试智能搜索接口
print("\nTesting smart search...")
try:
    response = requests.get("http://localhost:8001/api/search/smart?query=人工智能", timeout=30)
    print(f"Smart search status: {response.status_code}")
    print(f"Smart search response: {response.text}")
except Exception as e:
    print(f"Smart search error: {e}")
    import traceback
    traceback.print_exc()