<template>
  <div class="min-h-screen bg-surface font-body text-on-surface antialiased relative selection:bg-accent/20">
    <!-- 登录界面 -->
    <div v-if="!currentUser">
      <Login @login-success="handleLoginSuccess" />
    </div>

    <!-- 主应用内容 -->
    <div v-else>
      <!-- Toast Notification -->
      <div v-if="showToast" class="fixed top-24 left-1/2 -translate-x-1/2 z-[100] bg-on-surface text-surface px-6 py-3 rounded-full flex items-center gap-3 shadow-xl animate-fade-up">
        <span v-if="toastType === 'success'" class="material-symbols-outlined text-accent-teal">check_circle</span>
        <span v-else-if="toastType === 'warning'" class="material-symbols-outlined text-amber-400">warning</span>
        <span v-else-if="toastType === 'error'" class="material-symbols-outlined text-red-400">error</span>
        <span v-else class="material-symbols-outlined text-accent">info</span>
        <span class="text-sm font-bold">{{ toastMessage }}</span>
        <button @click="showToast = false" class="ml-2 hover:text-surface-muted">
          <span class="material-symbols-outlined text-sm">close</span>
        </button>
      </div>

      <!-- TopNavBar -->
      <nav v-if="currentView === 'discovery'" class="w-full sticky top-0 z-50 bg-[#FAFAFA]/90 backdrop-blur-md flex justify-between items-center px-6 md:px-12 py-4 md:py-6 max-w-screen-2xl mx-auto border-b border-outline-subtle/30">
        <div class="text-xl font-bold tracking-tighter text-on-surface font-headline border-2 border-on-surface px-2 py-0.5 rounded-md">SmartLib AI</div>
        <div class="hidden md:flex gap-8 items-center font-headline tracking-tight font-semibold">
          <a class="nav-link active" href="#">发现</a>
          <button @click="currentView = 'mylibrary'" class="nav-link cursor-pointer">我的书库</button>
          <button @click="currentView = 'dashboard'" class="nav-link cursor-pointer">管理大屏</button>
        </div>
        <div class="flex items-center gap-4">
          <div v-if="currentUser" class="flex items-center gap-3">
            <div class="text-right hidden sm:block">
              <p class="text-sm font-bold">{{ currentUser.username }}</p>
              <p class="text-xs text-on-surface-muted">{{ currentUser.email }}</p>
            </div>
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#0D9488] to-[#6366F1] flex items-center justify-center text-white font-bold">
              {{ currentUser.username ? currentUser.username.charAt(0).toUpperCase() : '' }}
            </div>
            <button @click="handleLogout" class="text-sm text-red-500 hover:text-red-600 font-medium">
              退出
            </button>
          </div>
        </div>
      </nav>

      <!-- C端搜索界面 -->
      <main v-if="currentView === 'discovery'" class="max-w-screen-2xl mx-auto px-6 md:px-12 py-8 md:py-12 flex flex-col gap-16 md:gap-24 relative">
        <!-- Hero Section -->
        <section class="flex flex-col items-center justify-center pt-8 pb-16 md:py-24 gap-8 animate-fade-up">
          <h1 class="text-4xl md:text-5xl lg:text-7xl font-extrabold font-headline tracking-tighter text-center max-w-4xl text-primary leading-[1.15]">
            为您，<span class="bg-clip-text text-transparent bg-gradient-to-r from-accent to-accent-teal">汇聚全球智慧。</span>
          </h1>
          <div class="w-full max-w-3xl relative mt-4">
            <div class="aurora-ring rounded-full p-1 shadow-aurora">
              <div class="flex items-center gap-4 px-6 md:px-8 py-4 md:py-5 bg-surface-card rounded-full relative z-10">
                <span class="material-symbols-outlined text-accent">auto_awesome</span>
                <input 
                  class="w-full bg-transparent border-none focus:ring-0 text-base md:text-lg placeholder-on-surface-muted/70 font-medium outline-none text-on-surface" 
                  placeholder="你今天在思考什么？告诉我你的心情..." 
                  type="text"
                  v-model="searchQuery"
                  @keyup.enter="performSearch"
                />
                <button @click="performSearch" v-if="!loading" class="material-symbols-outlined text-on-surface-muted hover:text-accent-teal transition-colors cursor-pointer bg-surface-low p-2 rounded-full">search</button>
                <div v-else class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-accent"></div>
              </div>
            </div>
            <div class="absolute -bottom-16 left-1/2 -translate-x-1/2 flex gap-3 overflow-x-auto whitespace-nowrap pb-2 no-scrollbar w-full justify-center">
              <span class="text-xs font-semibold tracking-wider text-on-surface-muted flex gap-3 items-center flex-wrap justify-center">
                <span class="material-symbols-outlined text-[14px] text-orange-500">local_fire_department</span> 热搜标签：
                <button @click="searchQuery = '治愈系'; performSearch()" class="px-3 py-1 bg-surface-low hover:bg-accent-teal hover:text-white border border-outline-subtle rounded-full cursor-pointer font-bold transition-all shadow-sm">#治愈系</button> 
                <button @click="searchQuery = '考研政治'; performSearch()" class="px-3 py-1 bg-surface-low hover:bg-accent-teal hover:text-white border border-outline-subtle rounded-full cursor-pointer font-bold transition-all shadow-sm">#考研政治</button> 
                <button @click="searchQuery = '单片机底层'; performSearch()" class="px-3 py-1 bg-surface-low hover:bg-accent-teal hover:text-white border border-outline-subtle rounded-full cursor-pointer font-bold transition-all shadow-sm">#单片机底层</button>
                <button @click="searchQuery = '太空史诗'; performSearch()" class="px-3 py-1 bg-surface-low hover:bg-accent-teal hover:text-white border border-outline-subtle rounded-full cursor-pointer font-bold transition-all shadow-sm">#太空史诗</button>
              </span>
            </div>
          </div>
        </section>

        <!-- 搜索状态与错误 -->
        <div v-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl text-center max-w-xl mx-auto border border-red-100 font-medium animate-scale-in">
          {{ error }}
        </div>

        <!-- Discovery Layout: Content + Smart Sidebar -->
        <div v-if="books.length > 0 || !searchQuery" class="flex flex-col xl:flex-row gap-12 xl:gap-20">
          <!-- Discovery Grid -->
          <div class="flex-grow">
              <!-- 推荐理由 -->
              <div v-if="recommendation" class="mb-10 p-6 bg-gradient-to-r from-accent/5 to-accent-teal/5 border border-accent/10 rounded-2xl animate-fade-up">
                <div class="flex items-start gap-4">
                  <span class="material-symbols-outlined text-accent mt-0.5">tips_and_updates</span>
                  <div>
                    <h3 class="text-xs font-extrabold text-accent mb-2 font-headline tracking-widest uppercase">AI 深度洞察</h3>
                    <p class="text-on-surface-muted leading-relaxed font-medium">{{ recommendation }}</p>
                  </div>
                </div>
              </div>

              <div v-if="books.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-12">
                <BookCard
                  v-for="(book, index) in books"
                  :key="book.isbn || index"
                  :book="book"
                  :featured="index === 0"
                  :show-recommendation="searchMode === 'smart'"
                  :current-user="currentUser"
                  :class="{'md:col-span-2': index === 0}"
                  class="animate-fade-up"
                  :style="{ animationDelay: index * 100 + 'ms' }"
                  @added-to-library="handleAddedToLibrary"
                  @show-toast="handleShowToast"
                />
              </div>
              
              <!-- Default mock content if no search results yet but app loaded -->
              <div v-if="books.length === 0 && !loading" class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-12 opacity-60 grayscale pointer-events-none filter blur-[2px] select-none transition-all duration-700">
                 <div class="md:col-span-2 card p-0 overflow-hidden flex flex-col md:flex-row gap-0">
                    <div class="w-full md:w-2/5 aspect-[3/4] bg-surface-low border-r border-outline-subtle"></div>
                    <div class="p-8 md:p-12 w-full md:w-3/5 flex flex-col justify-center gap-6">
                      <div class="h-4 bg-outline-subtle rounded-full w-1/4"></div>
                      <div class="h-10 bg-outline-subtle rounded-xl w-3/4"></div>
                      <div class="h-4 bg-outline-subtle rounded-full w-1/2"></div>
                      <div class="h-24 bg-outline-subtle rounded-xl w-full mt-4"></div>
                    </div>
                 </div>
                 <div class="card p-0 h-[400px] bg-surface-low rounded-2xl flex flex-col justify-end p-6">
                    <div class="h-6 bg-outline-subtle rounded-lg w-2/3 mb-4"></div>
                    <div class="h-4 bg-outline-subtle rounded-full w-1/2"></div>
                 </div>
                 <div class="card p-0 h-[400px] bg-surface-low rounded-2xl flex flex-col justify-end p-6">
                    <div class="h-6 bg-outline-subtle rounded-lg w-2/3 mb-4"></div>
                    <div class="h-4 bg-outline-subtle rounded-full w-1/2"></div>
                 </div>
              </div>
          </div>

          <!-- Smart Sidebar -->
          <aside class="w-full xl:w-96 flex flex-col gap-8 sticky top-24 h-fit animate-fade-up delay-300">
            <!-- Reading Preference Radar -->
            <div class="card p-8 flex flex-col gap-6">
              <div class="flex flex-col gap-1">
                <h5 class="font-headline font-extrabold text-lg flex items-center gap-2">
                  <span class="material-symbols-outlined text-accent-teal font-light">radar</span>
                  馆员洞察
                </h5>
                <p class="text-[10px] text-on-surface-muted uppercase tracking-widest font-bold">索书偏好雷达</p>
              </div>
              <div class="relative w-full aspect-square flex items-center justify-center">
                <svg viewBox="0 0 200 200" class="w-full h-full">
                  <!-- 同心参考圆 -->
                  <circle cx="100" cy="100" r="58" fill="none" stroke="currentColor" stroke-opacity="0.1" stroke-width="1" stroke-dasharray="3,4"/>
                  <circle cx="100" cy="100" r="43.5" fill="none" stroke="currentColor" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="3,4"/>
                  <circle cx="100" cy="100" r="29" fill="none" stroke="currentColor" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="3,4"/>
                  <circle cx="100" cy="100" r="14.5" fill="none" stroke="currentColor" stroke-opacity="0.06" stroke-width="1" stroke-dasharray="3,4"/>
                  <!-- 轴线 -->
                  <line v-for="(label, i) in radarAxes" :key="'axis-'+i"
                    :x1="100" :y1="100"
                    :x2="100 + 58 * Math.sin(i * Math.PI / 2)"
                    :y2="100 - 58 * Math.cos(i * Math.PI / 2)"
                    stroke="currentColor" stroke-opacity="0.12" stroke-width="1"/>
                  <!-- 数据多边形 -->
                  <polygon :points="radarPoints"
                    fill="rgba(13,148,136,0.15)" stroke="#0D9488" stroke-width="1.5" stroke-linejoin="round"/>
                  <!-- 数据点 -->
                  <circle v-for="(axis, i) in radarAxes" :key="'dot-'+i"
                    :cx="100 + 58 * axis.value * Math.sin(i * Math.PI / 2)"
                    :cy="100 - 58 * axis.value * Math.cos(i * Math.PI / 2)"
                    r="3" fill="#0D9488"/>
                  <!-- 轴标签 -->
                  <text v-for="(label, i) in radarLabels" :key="'label-'+i"
                    :x="label.x" :y="label.y"
                    text-anchor="middle" dominant-baseline="central"
                    class="text-[10px] font-extrabold uppercase tracking-widest"
                    fill="currentColor" fill-opacity="0.45"
                    style="font-family: inherit;">{{ label.label }}</text>
                </svg>
              </div>
              <div class="flex flex-col gap-3">
                <p class="text-sm text-on-surface-muted leading-relaxed font-medium" v-html="radarInsight"></p>
              </div>
            </div>

            <!-- Gemini Web Search Results -->
            <div v-if="webSearchResult" class="card p-8 flex flex-col gap-6 animate-fade-up">
              <div class="flex flex-col gap-1">
                <h5 class="font-headline font-extrabold text-lg flex items-center gap-2">
                  <span class="material-symbols-outlined text-accent-blue font-light">public</span> 
                  网络搜索
                </h5>
                <p class="text-[10px] text-on-surface-muted uppercase tracking-widest font-bold">Gemini 实时信息</p>
              </div>
              <div class="text-sm text-on-surface-muted leading-relaxed font-medium whitespace-pre-line">
                {{ webSearchResult }}
              </div>
            </div>

            <!-- Dynamic Tags -->
            <div class="flex flex-col gap-4">
              <h5 class="font-headline font-extrabold text-lg flex items-center gap-2">
                <span class="material-symbols-outlined text-accent font-light">hub</span>
                智慧节点
              </h5>
              <div class="flex flex-wrap gap-2">
                <span class="tag-pill text-[13px]"># 空间社会学</span>
                <span class="tag-pill text-[13px]"># 焦虑愈疗</span>
                <span class="tag-pill text-[13px]"># 后人类主义</span>
                <span class="tag-pill text-[13px]"># 城市生态学</span>
                <span class="tag-pill text-[13px]"># 极简主义</span>
              </div>
            </div>

            <!-- AI Premium CTA -->
            <div class="relative overflow-hidden bg-primary p-8 rounded-2xl text-white flex flex-col gap-4 shadow-xl border border-white/10 group cursor-pointer">
              <div class="absolute top-0 right-0 w-40 h-40 bg-gradient-to-br from-accent to-accent-teal opacity-40 blur-3xl rounded-full group-hover:scale-110 transition-transform duration-700"></div>
              <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-accent to-purple-500 opacity-20 blur-2xl rounded-full"></div>
              <span class="material-symbols-outlined text-3xl text-white relative z-10">diamond</span>
              <h6 class="text-xl font-bold font-headline relative z-10">解锁高级智能</h6>
              <p class="text-zinc-400 text-sm leading-relaxed relative z-10">
                为您书库中的所有文献提供深度引用交叉参考和情感倾向追踪。
              </p>
              <button class="mt-4 w-full py-3 bg-white text-primary font-bold rounded-xl hover:bg-surface-low transition-colors relative z-10">开启高级版</button>
            </div>
          </aside>
        </div>
        
        <div v-else-if="books.length === 0 && searchQuery && !loading" class="text-center py-24 animate-fade-up">
           <span class="material-symbols-outlined text-7xl text-outline-subtle mb-4 font-light">search_off</span>
           <h3 class="text-2xl font-bold font-headline mb-2 text-on-surface">未找到相关图书</h3>
           <p class="text-on-surface-muted">尝试更换更通用的关键词，或从右侧"智慧节点"中获取探索灵感。</p>
        </div>
      </main>

      <!-- SideNavBar (Mobile) -->
      <div v-if="currentView === 'discovery'" class="md:hidden fixed bottom-0 left-0 w-full bg-surface/90 backdrop-blur-xl z-[100] px-6 py-4 flex justify-around items-center border-t border-outline-subtle pb-safe shadow-[0_-10px_40px_rgba(0,0,0,0.05)]">
        <button class="flex flex-col items-center gap-1.5 text-on-surface">
          <span class="material-symbols-outlined text-[24px]">explore</span>
          <span class="text-[10px] font-extrabold uppercase tracking-wider">发现</span>
        </button>
        <button @click="currentView = 'mylibrary'" class="flex flex-col items-center gap-1.5 text-on-surface-muted hover:text-on-surface transition-colors">
          <span class="material-symbols-outlined text-[24px]">auto_stories</span>
          <span class="text-[10px] font-extrabold uppercase tracking-wider">书库</span>
        </button>
        <button @click="currentView = 'dashboard'" class="flex flex-col items-center gap-1.5 text-on-surface-muted hover:text-on-surface transition-colors">
          <span class="material-symbols-outlined text-[24px]">dashboard</span>
          <span class="text-[10px] font-extrabold uppercase tracking-wider">统计</span>
        </button>
      </div>

      <!-- B端仪表盘 -->
      <Dashboard v-if="currentView === 'dashboard'" @switch-to-search="currentView = 'discovery'" />
      <MyLibrary 
        v-if="currentView === 'mylibrary'" 
        :current-user="currentUser"
        @switch-to-search="currentView = 'discovery'" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BookCard from './components/BookCard.vue'
import Dashboard from './components/Dashboard.vue'
import MyLibrary from './components/MyLibrary.vue'
import Login from './components/Login.vue'
import { supabase } from './supabase.js'

const currentUser = ref(null)
const currentView = ref('discovery')
const searchQuery = ref('')
const searchMode = ref('smart')
const books = ref([])
const loading = ref(false)
const error = ref('')
const recommendation = ref('')
const webSearchResult = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const libraryTagCounts = ref({})

// 雷达图数据：Top 4 标签 + 归一化数值
const radarAxes = computed(() => {
  const entries = Object.entries(libraryTagCounts.value)
  if (entries.length === 0) {
    return [
      { label: '科幻', value: 0 },
      { label: '文学', value: 0 },
      { label: '历史', value: 0 },
      { label: '哲学', value: 0 }
    ]
  }
  entries.sort((a, b) => b[1] - a[1])
  const top4 = entries.slice(0, 4)
  const maxCount = top4[0]?.[1] || 1
  return top4.map(([tag, count]) => ({ label: tag, value: count / maxCount }))
})

// SVG 雷达多边形点
const radarPoints = computed(() => {
  return radarAxes.value.map((axis, i) => {
    const angle = (i * Math.PI) / 2
    const r = 58 * axis.value
    const x = 100 + r * Math.sin(angle)
    const y = 100 - r * Math.cos(angle)
    return `${x},${y}`
  }).join(' ')
})

// 雷达轴标签位置
const radarLabels = computed(() => {
  return radarAxes.value.map((axis, i) => {
    const angle = (i * Math.PI) / 2
    const r = 78
    const x = 100 + r * Math.sin(angle)
    const y = 100 - r * Math.cos(angle)
    return { ...axis, x, y }
  })
})

// 洞察文字
const radarInsight = computed(() => {
  if (radarAxes.value.every(a => a.value === 0)) {
    return '添加图书到书库后，我们会根据您的偏好生成个性化洞察。'
  }
  const top = radarAxes.value[0]
  return `您的关注点正转向 <span class="text-on-surface font-bold border-b-2 border-accent/30 pb-0.5">${top.label}</span>。我们已调整您的书库简报，加入更多相关内容。`
})

// 从标签中提取并统计
const collectTags = (tags) => {
  if (!tags || !Array.isArray(tags)) return
  const counts = { ...libraryTagCounts.value }
  for (const tag of tags) {
    counts[tag] = (counts[tag] || 0) + 1
  }
  libraryTagCounts.value = counts
}

// 从 Supabase 加载书库中的标签
const loadLibraryTags = async () => {
  if (!currentUser.value) return
  try {
    const { data, error } = await supabase
      .from('library_books')
      .select('title, author')
      .eq('user_id', String(currentUser.value.id))
    if (error || !data) return

    // 用书名在 mock_data 中查找标签（前端无法直接访问后端数据）
    // 主要通过 handleAddedToLibrary 实时累积
    const counts = {}
    for (const book of data) {
      // 尝试从搜索结果中已有的 books 匹配标签
      const matched = books.value.find(b => b.title === book.title)
      if (matched && matched.tags) {
        for (const tag of matched.tags) {
          counts[tag] = (counts[tag] || 0) + 1
        }
      }
    }
    if (Object.keys(counts).length > 0) {
      libraryTagCounts.value = { ...libraryTagCounts.value, ...counts }
    }
  } catch {}
}

const handleLoginSuccess = (user) => {
  currentUser.value = user
  currentView.value = 'discovery'
  toastMessage.value = '欢迎回来，' + user.username + '！'
  toastType.value = 'success'
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const handleLogout = () => {
  localStorage.removeItem('currentUser')
  currentUser.value = null
  toastMessage.value = '已退出登录'
  toastType.value = 'info'
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const handleAddedToLibrary = (book) => {
  collectTags(book.tags)
  const converted = parseInt(localStorage.getItem('smartlib_converted_count') || '0') + 1
  localStorage.setItem('smartlib_converted_count', converted)
  toastMessage.value = '已成功加入书库：' + book.title
  toastType.value = 'success'
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const toastType = ref('success')

const handleShowToast = (toast) => {
  toastMessage.value = toast.message
  toastType.value = toast.type || 'info'
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const fetchWithTimeout = (url, timeoutMs = 12000) => {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  return fetch(url, { signal: controller.signal }).finally(() => clearTimeout(timer))
}

const performSearch = async () => {
  if (!searchQuery.value.trim()) return

  // 追踪搜索指标
  const count = parseInt(localStorage.getItem('smartlib_search_count') || '0') + 1
  localStorage.setItem('smartlib_search_count', count)

  loading.value = true
  error.value = ''
  books.value = []
  recommendation.value = ''
  webSearchResult.value = ''

  try {
      const endpoint = searchMode.value === 'exact' 
        ? '/api/search/exact' 
        : '/api/search/smart'
    
    try {
      const apiBase = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8001'
      const response = await fetchWithTimeout(apiBase + endpoint + '?query=' + encodeURIComponent(searchQuery.value), 15000)
      if (!response.ok) {
        throw new Error('Search failed')
      }
      const data = await response.json()
      console.log("[Search Success] Result count:", data.count)
      console.log("[Search Success] Web search result:", data.web_search)
      books.value = data.results || []
      
      try {
        const { error: sbError } = await supabase
          .from('ai_search_sessions')
          .insert([{ search_query: searchQuery.value }])
        if (sbError) console.error('[Supabase] 写入失败:', sbError.message, sbError.details)
      } catch (sbErr) {
        console.error('[Supabase] 连接异常:', sbErr.message || sbErr)
      }

      if (searchMode.value === 'smart') {
        if (data.recommendation) {
          recommendation.value = data.recommendation
        }
        if (data.web_search) {
          webSearchResult.value = data.web_search
        }
      }
      loading.value = false
    } catch (e) {
      console.warn("[Search Warning] Backend fetch failed, falling back to mock data.", e)
      try {
        const { error: sbError } = await supabase
          .from('ai_search_sessions')
          .insert([{ search_query: searchQuery.value }])
        if (sbError) console.error('[Supabase] 写入失败:', sbError.message, sbError.details)
      } catch (sbErr) {
        console.error('[Supabase] 连接异常:', sbErr.message || sbErr)
      }
      // 模拟数据回退（后端不可用时立即展示）
      let mockBooks = [
        { title: "三体", author: "刘慈欣", description: "一部硬科幻杰作，深刻质疑了人类在充满敌意的宇宙中的地位。鉴于您最近对时空物理学的关注，此书为您首选匹配。", call_number: "I247.5", status: "在馆", rating: "9.4" },
        { title: "基地", author: "艾萨克·阿西莫夫", description: "破解历史周期的数学密码，建立拯救文明的庞大史诗。", call_number: "I712.4", status: "在馆", rating: "9.1" },
        { title: "挪威的森林", author: "村上春树", description: "一场关于丧失与青春晚期乡愁的诗意旅程。", call_number: "I313.4", status: "借出", rating: "8.9" },
      ]

      if(searchQuery.value.includes('现代孤独感')) {
        mockBooks = [mockBooks[2], mockBooks[0]]
        recommendation.value = '基于您对「现代孤独感」的探索，为您推荐探讨个体在庞大宇宙与社会结构中寻找存在意义的作品。'
      } else if (searchQuery.value.includes('硬科幻')) {
        mockBooks = [mockBooks[0], mockBooks[1]]
        recommendation.value = '从您的复杂查询中，我们提取了物理学硬核推演与社会哲学的交叉维度，为您优先推荐这两部经典。'
      } else {
        recommendation.value = '这是一份基于您意图的智能分析结果（模拟演示模式）。探索这些跨越时空的知识节点吧。'
      }

      books.value = mockBooks
      loading.value = false
    }
  } catch (err) {
    error.value = "网络异常或服务未启动，无法获取真实数据。"
    loading.value = false
  }
}

const loadDiscoveryBooks = async () => {
  loading.value = true
  const cacheKey = 'discovery_books_cache'

  // 1. 优先展示缓存，实现秒开
  const cached = localStorage.getItem(cacheKey)
  if (cached) {
    try {
      const parsed = JSON.parse(cached)
      if (parsed.length > 0) {
        books.value = parsed
        loading.value = false
      }
    } catch {}
  }

  // 2. 后台请求快速发现端点（不经过 LLM，秒级响应）
  try {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8001'
    const response = await fetchWithTimeout(apiBase + '/api/discovery', 8000)
    if (response.ok) {
      const data = await response.json()
      if (data.results && data.results.length > 0) {
        books.value = data.results
        localStorage.setItem(cacheKey, JSON.stringify(data.results))
        loading.value = false
        return
      }
    }
  } catch(e) {
    console.warn('[Discovery] Backend fetch failed:', e.message || e)
  }

  // 3. 后端不可用且无缓存时，立即展示模拟数据
  if (books.value.length === 0) {
    books.value = [
      { title: "三体", author: "刘慈欣", description: "一部硬科幻杰作，深刻质疑了人类在充满敌意的宇宙中的地位。鉴于您最近对时空物理学的关注，此书为您首选匹配。", call_number: "I247.5", status: "在馆", rating: "9.4" },
      { title: "基地", author: "艾萨克·阿西莫夫", description: "破解历史周期的数学密码，建立拯救文明的庞大史诗。", call_number: "I712.4", status: "在馆", rating: "9.1" },
      { title: "挪威的森林", author: "村上春树", description: "一场关于丧失与青春晚期乡愁的诗意旅程。", call_number: "I313.4", status: "借出", rating: "8.9" },
    ]
  }
  loading.value = false
}

// 组件加载时检查用户登录状态
onMounted(() => {
  const savedUser = localStorage.getItem('currentUser')
  if (savedUser) {
    currentUser.value = JSON.parse(savedUser)
  }
  loadDiscoveryBooks()
  loadLibraryTags()
})
</script>

<style scoped>
/* Scoped overrides if any */
</style>