# SmartLib AI - 后端

## 项目介绍

SmartLib AI 后端是一个基于 FastAPI 构建的智能图书检索与推荐系统后端服务，提供智能搜索、推荐和数据分析功能。系统集成了大模型能力，支持联网搜索和智能推荐。

## 技术栈

- **框架**：FastAPI
- **语言**：Python 3.10+
- **数据库**：SQLite (本地开发)
- **向量搜索**：TF-IDF + 余弦相似度
- **大模型**：
  - Gemini 1.5 Pro (优先)
  - DeepSeek V3 (备用)
- **部署**：Uvicorn
- **依赖管理**：pip

## 项目结构

```
backend/
├── main.py                    # 主应用入口
├── mock_data.json             # 模拟图书数据
├── embed_books.py             # 图书向量嵌入脚本
├── book_index.json            # 图书索引文件
├── .env                       # 环境变量配置
├── requirements.txt           # 依赖列表
├── README.md                  # 项目说明
└── test_api.html              # API测试页面
```

## 功能特性

### 核心功能
- **智能搜索**：基于TF-IDF向量搜索 + 大模型查询优化
- **联网搜索**：集成Gemini 1.5 Pro实现实时网络信息获取
- **图书推荐**：基于语义相似度的智能推荐
- **查询重写**：使用大模型优化用户查询意图
- **数据分析**：提供搜索趋势和系统运行数据

### API接口

#### 健康检查
- `GET /health` - 检查系统健康状态

#### 精确搜索
- `GET /api/search/exact?query=关键词` - 精确匹配图书标题和作者

#### 智能搜索
- `GET /api/search/smart?query=关键词` - 智能语义搜索，包含联网搜索结果

## 安装与运行

### 前置条件
- Python 3.10+
- pip 20.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

在 `.env` 文件中配置API密钥：

```env
# 大模型API配置
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 生成图书索引

```bash
python embed_books.py
```

### 运行开发服务器

```bash
python main.py
```

后端服务将运行在 `http://localhost:8000`

## API接口说明

### 智能搜索接口 (`/api/search/smart`)

**请求参数**：
- `query` (必填)：搜索关键词

**返回格式**：
```json
{
  "results": [
    {
      "isbn": "9787536692930",
      "title": "三体",
      "author": "刘慈欣",
      "description": "文化大革命如火如荼地进行...",
      "rating": 4.8,
      "call_number": "I247.55/1234",
      "status": "可借",
      "tags": ["科幻", "硬科幻", "中国文学"],
      "emotion": "震撼",
      "scenario": "深度阅读",
      "similar_books": [
        {
          "title": "三体2：黑暗森林",
          "rating": 4.9,
          "emotion": "紧张"
        }
      ]
    }
  ],
  "count": 3,
  "rewritten_query": "优化后的查询词",
  "web_search": "Gemini联网搜索结果",
  "recommendation": "智能推荐理由"
}
```

## 大模型集成

### Gemini 1.5 Pro
- **优势**：内置联网搜索能力，实时获取最新信息
- **用途**：查询重写、联网搜索、智能推荐
- **配置**：在 `.env` 中设置 `GEMINI_API_KEY`

### DeepSeek V3
- **优势**：响应速度快，适合中文处理
- **用途**：查询重写、推荐理由生成
- **配置**：在 `.env` 中设置 `DEEPSEEK_API_KEY`

## 数据结构

### 图书数据结构

```json
{
  "isbn": "9787536692930",
  "title": "三体",
  "author": "刘慈欣",
  "description": "图书描述",
  "rating": 4.8,
  "call_number": "I247.55/1234",
  "status": "可借",
  "tags": ["科幻", "硬科幻"],
  "emotion": "震撼",
  "scenario": "深度阅读"
}
```

## 开发建议

1. **环境管理**：使用虚拟环境隔离依赖
2. **日志管理**：系统会输出详细的搜索和推理日志
3. **性能优化**：对于大规模图书数据，考虑使用更高效的向量数据库
4. **安全管理**：API密钥应妥善保管，避免泄露
5. **错误处理**：系统已实现完善的错误处理机制

## 部署指南

### 生产环境部署

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**：
   - 设置真实的API密钥
   - 配置生产环境的数据库连接

3. **启动服务**：
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **反向代理**：
   - 使用 Nginx 或 Apache 作为反向代理
   - 配置 HTTPS 证书

### 容器化部署

可以使用 Docker 容器化部署：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV GEMINI_API_KEY=your_api_key
ENV DEEPSEEK_API_KEY=your_api_key

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 故障排查

### 常见问题

1. **API密钥错误**：检查 `.env` 文件中的API密钥是否正确
2. **端口占用**：确保8000端口未被其他服务占用
3. **依赖缺失**：运行 `pip install -r requirements.txt` 安装所有依赖
4. **网络问题**：确保服务器可以访问Gemini和DeepSeek API

### 日志查看

系统会在控制台输出详细的日志信息，包括：
- 搜索查询和结果
- 大模型调用情况
- 错误信息和异常

## 性能优化

1. **缓存机制**：对于频繁的查询结果进行缓存
2. **批量处理**：批量处理向量计算，提高性能
3. **异步处理**：使用FastAPI的异步特性处理并发请求
4. **模型选择**：根据需求选择合适的大模型，平衡速度和质量