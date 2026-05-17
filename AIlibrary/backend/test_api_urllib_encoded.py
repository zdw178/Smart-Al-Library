import urllib.request
import urllib.parse
import urllib.error

# 测试健康检查接口
print("Testing health check...")
try:
    response = urllib.request.urlopen("http://localhost:8001/health", timeout=10)
    print(f"Health check status: {response.status}")
    content = response.read().decode('utf-8')
    print(f"Health check response: {content}")
except urllib.error.URLError as e:
    print(f"Health check URLError: {e}")
except Exception as e:
    print(f"Health check error: {e}")
    import traceback
    traceback.print_exc()

# 测试智能搜索接口
print("\nTesting smart search...")
try:
    # 对中文字符进行URL编码
    query = urllib.parse.quote("人工智能")
    url = f"http://localhost:8001/api/search/smart?query={query}"
    print(f"Encoded URL: {url}")
    
    response = urllib.request.urlopen(url, timeout=30)
    print(f"Smart search status: {response.status}")
    content = response.read().decode('utf-8')
    print(f"Smart search response: {content}")
except urllib.error.URLError as e:
    print(f"Smart search URLError: {e}")
except Exception as e:
    print(f"Smart search error: {e}")
    import traceback
    traceback.print_exc()