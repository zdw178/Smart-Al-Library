# SmartLib AI - 前端

## 项目介绍

SmartLib AI 是一个基于大模型驱动的智能图书检索与推荐系统，为用户提供智能的图书搜索、推荐和管理功能。

## 技术栈

- **框架**：Vue 3 + Vite
- **语言**：JavaScript
- **样式**：Tailwind CSS
- **图表**：Chart.js + vue-chartjs
- **构建工具**：Vite
- **包管理**：npm

## 项目结构

```
frontend/
├── src/
│   ├── components/            # 组件目录
│   │   ├── BookCard.vue       # 图书卡片组件
│   │   └── Dashboard.vue      # 管理员仪表盘组件
│   ├── App.vue                # 主应用组件
│   ├── main.js                # 应用入口
│   └── style.css              # 全局样式
├── public/                    # 静态资源
├── index.html                 # HTML模板
├── package.json               # 项目配置
├── tailwind.config.js         # Tailwind配置
├── postcss.config.js          # PostCSS配置
├── vite.config.js             # Vite配置
└── README.md                  # 项目说明
```

## 功能特性

### 读者端 (C端)
- **智能搜索**：支持自然语言搜索，会自动纠正拼写和优化查询
- **图书推荐**：基于语义相似度和用户意图的智能推荐
- **图书卡片**：展示图书详细信息、评分、状态等
- **搜索历史**：记录搜索历史，方便重复搜索
- **响应式设计**：适配不同设备屏幕

### 管理员端 (B端)
- **数据仪表盘**：展示系统运行数据和统计信息
- **语义趋势**：展示搜索关键词的语义趋势分析
- **AI推理日志**：查看AI模型的推理记录和性能
- **系统状态**：监控系统运行状态

## 安装与运行

### 前置条件
- Node.js 18.0+
- npm 9.0+

### 安装依赖

```bash
npm install
```

### 开发模式运行

```bash
npm run dev
```

前端服务将运行在 `http://localhost:5173`

### 构建生产版本

```bash
npm run build
```

构建产物将生成在 `dist` 目录

## 环境配置

前端默认连接的后端API地址：`http://localhost:8000`

如果后端服务运行在不同地址，需要修改 `src/main.js` 中的API基础路径。

## 主要组件说明

### App.vue
主应用组件，包含路由切换、搜索界面和仪表盘界面。

### BookCard.vue
图书卡片组件，展示图书详细信息，支持不同样式的卡片展示。

### Dashboard.vue
管理员仪表盘组件，包含数据统计、趋势图表和AI推理日志。

## 样式设计

- **设计系统**：基于Tailwind CSS的现代化设计
- **配色方案**：清新的蓝色调，搭配白色和浅灰色
- **响应式**：移动端、平板、桌面端自适应
- **动画效果**：流畅的过渡动画和交互反馈

## 开发建议

1. **组件开发**：遵循Vue 3 Composition API的最佳实践
2. **样式管理**：使用Tailwind的工具类，避免自定义CSS
3. **性能优化**：合理使用Vue的响应式系统，避免不必要的重渲染
4. **代码规范**：遵循ESLint和Prettier的代码规范

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+