import requests
import json
import time

# 测试DeepSeek API
url = "https://api.siliconflow.cn/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-nyqkcrplrsggbftjqxsstoghrlecliwyfmmtdxabgrmvfczj"
}

payload = {
    "model": "deepseek-ai/DeepSeek-V3.2",
    "messages": [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好，请问你像看什么书呢"}
    ]
}

print("正在呼叫 DeepSeek，请稍候...")
print(f"请求URL: {url}")
print(f"请求头: {json.dumps(headers, indent=2)}")
print(f"请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    start_time = time.time()
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    end_time = time.time()
    
    print(f"\n响应时间: {end_time - start_time:.2f}秒")
    print(f"状态码: {response.status_code}")
    print(f"响应头: {json.dumps(dict(response.headers), indent=2)}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        # 扒开一层层的数据，拿到 AI 说的话
        ai_message = result["choices"][0]["message"]["content"]
        print("\nAI回复：\n", ai_message)
    else:
        print("调用失败！状态码:", response.status_code)
        print("错误信息:", response.text)
except requests.exceptions.RequestException as e:
    print(f"网络请求异常: {e}")
except Exception as e:
    print(f"发生异常: {e}")
    import traceback
    traceback.print_exc()