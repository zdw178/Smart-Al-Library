# SmartLib AI 前端UI设计代码文档

## 项目结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── BookCard.vue     # 图书卡片组件
│   │   └── Dashboard.vue    # 仪表盘组件
│   ├── App.vue              # 主应用组件
│   ├── main.js              # 应用入口
│   └── style.css            # 全局样式
├── index.html               # HTML模板
├── package.json             # 项目配置
├── tailwind.config.js       # Tailwind配置
└── vite.config.js           # Vite配置
```

## 核心组件代码

### 1. App.vue - 主应用组件

```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-white to-blue-50">
    <!-- C端搜索界面 -->
    <div v-if="!showDashboard">
      <!-- 顶部导航栏 -->
      <header class="bg-white shadow-sm">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 class="text-2xl font-bold text-blue-600">SmartLib AI</h1>
          <nav class="flex items-center space-x-6">
            <a href="#" class="text-blue-600 font-medium">发现</a>
            <a href="#" class="text-gray-600 hover:text-blue-600">我的书库</a>
            <button 
              @click="showDashboard = true"
              class="text-gray-600 hover:text-blue-600 font-medium"
            >
              管理大屏
            </button>
          </nav>
          <div class="flex items-center">
            <button class="p-2 rounded-full hover:bg-gray-100">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- 主要内容区 -->
      <main class="container mx-auto px-4 py-8">
        <!-- 标题区域 -->
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-2">
            <span class="text-gray-800">为您，</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">汇聚全球智慧</span>
          </h2>
          <p class="text-gray-600 mt-2">探索知识的无限可能</p>
        </div>

        <!-- 搜索区域 -->
        <div class="max-w-3xl mx-auto mb-12">
          <!-- 搜索框 -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <div class="flex items-center space-x-2">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                <span class="text-sm text-gray-500">AI</span>
              </div>
            </div>
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="performSearch"
              placeholder="你今天在思考什么？告诉我你的心情..."
              class="block w-full p-4 pl-16 pr-4 text-lg border border-gray-300 rounded-full shadow-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              @click="performSearch"
              class="absolute inset-y-0 right-2 flex items-center"
            >
              <button
                type="button"
                class="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 focus:ring-4 focus:ring-blue-300"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </button>
            </button>
          </div>
          <!-- 搜索范围标签 -->
          <div class="flex justify-center mt-4 space-x-4">
            <span class="text-xs text-gray-500">搜索范围：</span>
            <button class="text-xs text-blue-600 hover:underline">现代通信</button>
            <span class="text-xs text-gray-400">|</span>
            <button class="text-xs text-blue-600 hover:underline">硬科幻黑色系</button>
            <span class="text-xs text-gray-400">|</span>
            <button class="text-xs text-blue-600 hover:underline">从神话到哲学思辨</button>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="mt-4 flex justify-center">
          <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {{ error }}
        </div>

        <!-- 推荐理由（仅AI模式） -->
        <div v-if="recommendation" class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg class="w-6 h-6 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-800">AI 推荐理由</h3>
              <div class="mt-2 text-sm text-blue-700">
                <p>{{ recommendation }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 图书卡片列表 -->
        <div v-if="books.length > 0" class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <BookCard
            v-for="book in books"
            :key="book.isbn"
            :book="book"
            :show-recommendation="searchMode === 'smart'"
          />
        </div>

        <!-- 无结果提示 -->
        <div v-if="!loading && books.length === 0 && searchQuery" class="mt-8 text-center">
          <p class="text-gray-600">未找到相关图书</p>
        </div>
      </main>

      <!-- 页脚 -->
      <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-4 py-4 text-center text-gray-600">
          <p>© 2026 SmartLib AI - 智慧校园大模型驱动图书检索与推荐系统</p>
        </div>
      </footer>
    </div>

    <!-- B端仪表盘 -->
    <Dashboard v-else @switch-to-search="showDashboard = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BookCard from './components/BookCard.vue'
import Dashboard from './components/Dashboard.vue'

const showDashboard = ref(false)
const searchQuery = ref('')
const searchMode = ref('exact')
const books = ref([])
const loading = ref(false)
const error = ref('')
const recommendation = ref('')

const performSearch = async () => {
  if (!searchQuery.value.trim()) return

  loading.value = true
  error.value = ''
  books.value = []
  recommendation.value = ''

  try {
    const endpoint = searchMode.value === 'exact' 
      ? '/api/search/exact' 
      : '/api/search/smart'
    
    const response = await fetch(`http://127.0.0.1:8000${endpoint}?query=${encodeURIComponent(searchQuery.value)}`)
    
    if (!response.ok) {
      throw new Error('搜索失败，请稍后重试')
    }

    const data = await response.json()
    books.value = data.results || []
    
    if (searchMode.value === 'smart' && data.recommendation) {
      recommendation.value = data.recommendation
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* App styles */
</style>
```

### 2. BookCard.vue - 图书卡片组件

```vue
<template>
  <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
    <!-- 封面图片 -->
    <div class="relative h-64 overflow-hidden">
      <img 
        :src="getBookCover(book.title)" 
        :alt="book.title"
        class="w-full h-full object-cover"
      />
      <!-- 标签 -->
      <div class="absolute top-2 right-2 flex space-x-2">
        <span class="px-2 py-1 bg-blue-600 text-white text-xs rounded">AI推荐</span>
        <span class="px-2 py-1 bg-gray-800 text-white text-xs rounded">豆瓣 {{ book.rating }}</span>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="p-4">
      <!-- 书名和作者 -->
      <h3 class="text-xl font-bold text-gray-900 mb-1">{{ book.title }}</h3>
      <p class="text-gray-600 text-sm mb-3">{{ book.author }}</p>

      <!-- AI推荐理由 -->
      <div v-if="showRecommendation" class="mb-4">
        <div class="flex items-start">
          <div class="flex-shrink-0 mr-2">
            <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            <svg class="w-4 h-4 text-purple-500 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
          <p class="text-sm text-gray-700">
            通过宇宙社会学探讨现代生存的荒诞性。
          </p>
        </div>
      </div>

      <!-- 简介 -->
      <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ book.description }}</p>

      <!-- 索书号和状态 -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <span class="text-xs text-gray-500">索书号：</span>
          <span class="text-sm font-medium text-gray-700">{{ book.call_number }}</span>
        </div>
        <span :class="[
          'px-2 py-1 text-xs rounded-full',
          book.status === '在馆' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
          {{ book.status }}
        </span>
      </div>

      <!-- 操作按钮 -->
      <div class="flex space-x-2">
        <button class="flex-1 px-3 py-2 bg-gray-100 text-gray-800 text-sm rounded hover:bg-gray-200">
          阅读分析
        </button>
        <button class="flex-1 px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
          加入书库
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  book: {
    type: Object,
    required: true
  },
  showRecommendation: {
    type: Boolean,
    default: false
  }
})

// 生成图书封面图片
const getBookCover = (title) => {
  // 使用不同的封面图片URL，根据书名生成不同的封面
  const covers = [
    'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=science%20fiction%20book%20cover%20with%20space%20and%20cosmos&image_size=portrait_4_3',
    'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=foundation%20book%20cover%20with%20golden%20rings&image_size=portrait_4_3',
    'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=norwegian%20wood%20book%20cover%20with%20forest&image_size=portrait_4_3',
    'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=programming%20book%20cover%20with%20code&image_size=portrait_4_3',
    'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=economics%20book%20cover%20with%20charts&image_size=portrait_4_3'
  ]
  
  // 根据书名的哈希值选择封面
  let hash = 0
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % covers.length
  return covers[index]
}
</script>

<style scoped>
/* BookCard styles */
</style>
```

### 3. Dashboard.vue - 仪表盘组件

```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-white to-blue-50">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-blue-600">SmartLib AI</h1>
        <nav class="flex items-center space-x-6">
          <a href="#" class="text-gray-600 hover:text-blue-600">内容探索</a>
          <a href="#" class="text-gray-600 hover:text-blue-600">我的书库</a>
          <a href="#" class="text-blue-600 font-medium">管理面板</a>
        </nav>
        <div class="flex items-center">
          <button class="p-2 rounded-full hover:bg-gray-100">
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- 主要内容区 -->
    <main class="container mx-auto px-4 py-8">
      <!-- 标题区域 -->
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-800">馆长智慧</h2>
        <p class="text-gray-600 mt-2">实时监测图书馆数字学识，提供RAG诊断与语义需求预测。</p>
      </div>

      <!-- 顶部数据卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- 今日AI检索人次 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm text-gray-500">AI 检索会话</p>
              <h3 class="text-3xl font-bold text-gray-800 mt-1">{{ metrics.todaySearches.toLocaleString() }}</h3>
              <p class="text-xs text-green-600 mt-2">↑ 较上期增长 12.4%</p>
            </div>
            <div class="p-2 bg-blue-100 rounded-full">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- 意图识别准确率 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm text-gray-500">意图识别准确率</p>
              <h3 class="text-3xl font-bold text-gray-800 mt-1">{{ metrics.accuracyRate }}%</h3>
              <div class="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                <div class="bg-green-500 h-1.5 rounded-full" :style="{ width: metrics.accuracyRate + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 借阅转化率 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm text-gray-500">借阅转化率</p>
              <h3 class="text-3xl font-bold text-gray-800 mt-1">{{ metrics.conversionRate }}%</h3>
              <p class="text-xs text-gray-600 mt-2">达到预期最优分配状态</p>
            </div>
            <div class="p-2 bg-purple-100 rounded-full">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间图表区 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- 语义趋势分析 -->
        <div class="bg-white rounded-lg shadow-md p-6 lg:col-span-2">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-bold text-gray-800">语义趋势分析</h2>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-xs bg-blue-600 text-white rounded">7天</button>
              <button class="px-3 py-1 text-xs bg-gray-200 text-gray-800 rounded">30天</button>
            </div>
          </div>
          <div class="h-64">
            <Bar
              :data="chartData"
              :options="chartOptions"
            />
          </div>
        </div>

        <!-- 右侧信息区 -->
        <div class="space-y-6">
          <!-- 馆员洞察 -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-sm font-medium text-gray-500 mb-3">馆员洞察</h3>
            <div class="bg-gray-100 p-4 rounded-md">
              <p class="text-xs text-gray-600 mb-2">阅读偏好</p>
              <div class="flex justify-between items-center">
                <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-purple-500 rounded-md flex items-center justify-center">
                  <span class="text-white font-medium">哲学</span>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-800">32%</p>
                  <p class="text-xs text-gray-500">较上月 +5%</p>
                </div>
              </div>
              <p class="text-xs text-gray-600 mt-4">数据洞察</p>
              <p class="text-xs text-gray-700 mt-1">
                部分关注工程学科的学生小组进入沉浸式阅读的深度学习状态增长了40%，建议扩大"技术理性"相关采购。
              </p>
              <button class="mt-3 px-3 py-1 text-xs bg-blue-100 text-blue-600 rounded">生成采购计划</button>
            </div>
          </div>

          <!-- 智慧节点 -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-sm font-medium text-gray-500 mb-3">智慧节点</h3>
            <div class="flex flex-wrap gap-2">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">空间社会学</span>
              <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">虚拟客厅</span>
              <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">后人类主义</span>
              <span class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded">城市生态字</span>
              <span class="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">结构主义</span>
            </div>
            <div class="mt-4 p-4 bg-gray-900 rounded-md">
              <h4 class="text-sm font-medium text-white mb-2">解锁高级智能</h4>
              <p class="text-xs text-gray-300 mb-3">为柜书中心的所有藏品提供深度引用交叉索引和情感脉络追踪。</p>
              <button class="w-full px-3 py-2 bg-white text-gray-900 text-xs rounded hover:bg-gray-100">开启高级版</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部日志监控区 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-bold text-gray-800">AI 推理审计</h2>
          <div class="flex items-center space-x-4">
            <span class="text-xs text-gray-500">实时性能诊断中</span>
            <button class="text-xs text-blue-600 hover:underline">查看历史记录</button>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 font-medium text-gray-500">用户查询意图</th>
                <th class="text-left py-3 px-4 font-medium text-gray-500">RAG 提取关键词</th>
                <th class="text-left py-3 px-4 font-medium text-gray-500">推荐主题路径</th>
                <th class="text-left py-3 px-4 font-medium text-gray-500">置信度</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(log, index) in logs" :key="index" class="border-b border-gray-200">
                <td class="py-3 px-4">
                  <p class="text-gray-800">{{ log.question }}</p>
                  <p class="text-xs text-gray-500">意图: 存在主义</p>
                </td>
                <td class="py-3 px-4">
                  <div class="flex flex-wrap gap-1">
                    <span v-for="(tag, tagIndex) in log.tags" :key="tagIndex" class="px-2 py-0.5 bg-gray-100 text-gray-800 text-xs rounded">
                      {{ tag }}
                    </span>
                  </div>
                </td>
                <td class="py-3 px-4">
                  <p class="text-gray-800">{{ log.recommendation }}</p>
                  <p class="text-xs text-gray-500">在库: 1027 存/存在与时间</p>
                </td>
                <td class="py-3 px-4">
                  <div class="flex items-center">
                    <div class="w-16 bg-gray-200 rounded-full h-1.5 mr-2">
                      <div class="bg-green-500 h-1.5 rounded-full" style="width: 98%"></div>
                    </div>
                    <span class="text-xs font-medium text-gray-800">0.98</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-4 flex justify-between items-center">
          <div class="text-xs text-gray-500">
            系统异常: <span class="text-green-600">无异常</span>
          </div>
          <button class="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700">
            我要调优检索
          </button>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="bg-white border-t mt-12">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <p class="text-gray-600">© 2026 SmartLib AI - 智慧校园大模型驱动图书检索与推荐系统</p>
        <button 
          @click="$emit('switchToSearch')"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          返回搜索界面
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// 注册Chart.js组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

// 定义props和emits
const emit = defineEmits(['switchToSearch'])

// 模拟数据
const metrics = ref({
  todaySearches: 128,
  searchGrowth: 12.5,
  conversionRate: 32.8,
  conversionGrowth: 3.2,
  accuracyRate: 94.5,
  accuracyGrowth: 1.8
})

// 图表数据
const chartData = ref({
  labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
  datasets: [
    {
      label: '单片机开发',
      data: [12, 19, 15, 20, 25, 30, 22],
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    },
    {
      label: '科幻文学',
      data: [28, 25, 30, 35, 40, 32, 28],
      backgroundColor: 'rgba(153, 102, 255, 0.6)',
      borderColor: 'rgba(153, 102, 255, 1)',
      borderWidth: 1
    },
    {
      label: '考研',
      data: [8, 12, 10, 15, 18, 20, 15],
      backgroundColor: 'rgba(255, 206, 86, 0.6)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 1
    },
    {
      label: '经济学',
      data: [15, 18, 22, 19, 25, 28, 20],
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }
  ]
})

// 图表配置
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true
    }
  },
  plugins: {
    legend: {
      position: 'top'
    }
  }
})

// 日志数据
const logs = ref([
  {
    question: '想看探讨宇宙社会的科幻书',
    tags: ['科幻', '宇宙', '社会'],
    recommendation: '推荐《三体》、《三体Ⅱ：黑暗森林》、《三体Ⅲ：死神永生》',
    time: '14:30:25'
  },
  {
    question: '推荐一本Arduino入门书籍',
    tags: ['Arduino', '单片机', '入门'],
    recommendation: '推荐《Arduino从入门到精通》',
    time: '14:25:10'
  },
  {
    question: '经济学原理相关的书籍',
    tags: ['经济学', '原理'],
    recommendation: '推荐《经济学原理》、《宏观经济学》',
    time: '14:20:45'
  },
  {
    question: '中国古典四大名著',
    tags: ['古典文学', '四大名著'],
    recommendation: '推荐《红楼梦》、《西游记》、《水浒传》、《三国演义》',
    time: '14:15:30'
  },
  {
    question: '关于人工智能的书籍',
    tags: ['人工智能'],
    recommendation: '推荐《人类简史》、《未来简史》',
    time: '14:10:15'
  }
])

// 当前日期
const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

// 模拟实时日志更新
onMounted(() => {
  setInterval(() => {
    // 模拟新日志
    const newLog = {
      question: '推荐一本关于时间旅行的科幻小说',
      tags: ['科幻', '时间旅行'],
      recommendation: '推荐《时间简史》',
      time: new Date().toLocaleTimeString('zh-CN')
    }
    logs.value.unshift(newLog)
    // 保持日志数量在5条
    if (logs.value.length > 5) {
      logs.value.pop()
    }
  }, 10000) // 每10秒更新一次
})
</script>

<style scoped>
/* Dashboard styles */
</style>
```

## 技术栈

- **前端框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **CSS框架**: Tailwind CSS
- **图表库**: Chart.js + vue-chartjs
- **HTTP请求**: 原生fetch API

## 设计特点

1. **现代化UI设计**:
   - 使用渐变色和阴影效果
   - 响应式布局
   - 卡片式设计
   - 简洁明了的视觉层次

2. **用户体验**:
   - 流畅的页面切换
   - 清晰的搜索界面
   - 详细的图书信息展示
   - 数据可视化仪表盘

3. **功能完整**:
   - C端搜索功能
   - B端数据统计
   - AI推荐系统
   - 实时日志监控

## 如何使用

1. **安装依赖**:
   ```bash
   npm install
   ```

2. **启动开发服务器**:
   ```bash
   npm run dev
   ```

3. **访问应用**:
   - 前端: http://localhost:5173
   - 后端: http://127.0.0.1:8000

4. **功能测试**:
   - 在搜索框中输入关键词进行搜索
   - 切换到"管理大屏"查看数据统计
   - 体验AI推荐功能
