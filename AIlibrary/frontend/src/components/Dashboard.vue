<template>
  <div class="animate-fade-up min-h-screen bg-surface">
    <!-- 顶部导航条 -->
    <nav class="w-full bg-surface-card/90 backdrop-blur-md border-b border-outline-subtle sticky top-0 z-50">
      <div class="container mx-auto px-6 md:px-12 py-4 flex justify-between items-center max-w-screen-2xl">
        <h1 class="text-xl font-bold font-headline tracking-tight text-on-surface flex items-center gap-2">
          <span class="material-symbols-outlined text-accent" style="font-variation-settings: 'FILL' 1;">analytics</span>
          馆长智慧屏
        </h1>
        <div class="flex items-center gap-4">
           <button @click="$emit('switchToSearch')" class="btn-outline py-2 px-5 border-outline-subtle text-sm flex gap-2 items-center hover:text-accent hover:border-accent/30 transition-colors">
             <span class="material-symbols-outlined text-[18px]">arrow_back</span>
             返回发现
           </button>
        </div>
      </div>
    </nav>
    
    <main class="container mx-auto px-6 md:px-12 py-10 max-w-screen-2xl flex flex-col gap-10">
      <!-- Header -->
      <div class="flex flex-col gap-3">
        <h2 class="text-3xl md:text-5xl font-extrabold font-headline leading-tight tracking-tighter">数字学识监测中心</h2>
        <p class="text-on-surface-muted font-medium flex items-center gap-2 text-sm md:text-base">
           实时监测图书馆数字学识，提供 <span class="px-2 py-0.5 rounded text-xs font-bold font-mono bg-accent/10 border border-accent/20 text-accent mx-1">RAG</span> 诊断与语义需求预测
           <span class="live-dot ml-1"></span>
        </p>
      </div>

      <!-- KPIs -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Metric 1 -->
        <div class="metric-card bg-gradient-to-br from-surface-card to-accent/5 border border-accent/10 relative overflow-hidden group">
          <div class="absolute -right-4 -top-4 w-24 h-24 bg-accent/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-700"></div>
          <div class="flex justify-between items-start mb-6 relative z-10">
             <div class="p-3 bg-white/80 backdrop-blur rounded-xl shadow-sm border border-outline-subtle/50 text-accent">
                <span class="material-symbols-outlined">forum</span>
             </div>
             <span class="px-2.5 py-1 bg-emerald-50 border border-emerald-100 text-emerald-700 rounded text-[11px] font-bold font-mono tracking-widest">+12.4%</span>
          </div>
          <p class="text-xs text-on-surface-muted font-extrabold tracking-widest uppercase mb-1 relative z-10">今日 AI 检索会话</p>
          <h3 class="text-4xl md:text-5xl font-extrabold font-headline text-on-surface relative z-10">{{ metrics.todaySearches.toLocaleString() }}</h3>
        </div>

        <!-- Metric 2 -->
        <div class="metric-card bg-gradient-to-br from-surface-card to-emerald-500/5 border border-emerald-500/10 relative overflow-hidden group">
          <div class="absolute -right-4 -top-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-700"></div>
          <div class="flex justify-between items-start mb-6 relative z-10">
             <div class="p-3 bg-white/80 backdrop-blur rounded-xl shadow-sm border border-outline-subtle/50 text-emerald-600">
                <span class="material-symbols-outlined">api</span>
             </div>
          </div>
          <p class="text-xs text-on-surface-muted font-extrabold tracking-widest uppercase mb-1 relative z-10">意图识别准确率</p>
          <div class="flex items-end gap-3 mb-3 relative z-10">
             <h3 class="text-4xl md:text-5xl font-extrabold font-headline text-on-surface">{{ metrics.accuracyRate }}%</h3>
          </div>
          <div class="w-full bg-surface-high rounded-full h-1.5 overflow-hidden relative z-10">
            <div class="bg-gradient-to-r from-emerald-400 to-emerald-600 h-1.5 rounded-full" :style="{ width: metrics.accuracyRate + '%' }"></div>
          </div>
        </div>

        <!-- Metric 3 -->
        <div class="metric-card bg-gradient-to-br from-surface-card to-accent-teal/5 border border-accent-teal/10 relative overflow-hidden group">
          <div class="absolute -right-4 -top-4 w-24 h-24 bg-accent-teal/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-700"></div>
          <div class="flex justify-between items-start mb-6 relative z-10">
             <div class="p-3 bg-white/80 backdrop-blur rounded-xl shadow-sm border border-outline-subtle/50 text-accent-teal">
                <span class="material-symbols-outlined">library_books</span>
             </div>
          </div>
          <p class="text-xs text-on-surface-muted font-extrabold tracking-widest uppercase mb-1 relative z-10">借阅转化率</p>
          <h3 class="text-4xl md:text-5xl font-extrabold font-headline text-on-surface mb-2 relative z-10">{{ metrics.conversionRate }}%</h3>
          <p class="text-[11px] text-accent-teal font-extrabold tracking-wider uppercase mt-auto relative z-10">达到预期最优分配状态</p>
        </div>
      </div>

      <!-- Charts & Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
         <!-- Chart -->
         <div class="card p-6 md:p-8 lg:col-span-2 border border-outline-subtle flex flex-col gap-6">
            <div class="flex justify-between items-center border-b border-outline-subtle/50 pb-4">
              <h3 class="text-xl font-bold font-headline flex items-center gap-2 text-on-surface">
                <span class="material-symbols-outlined text-accent font-light">monitoring</span>
                语义趋势分析
              </h3>
              <div class="flex bg-surface-low p-1 rounded-lg">
                 <button class="px-4 py-1.5 bg-white shadow-sm rounded text-xs font-bold text-on-surface transition-all">7天</button>
                 <button class="px-4 py-1.5 rounded text-xs font-bold text-on-surface-muted hover:text-on-surface transition-all">30天</button>
              </div>
            </div>
            <div class="h-[320px] w-full pt-2">
               <Bar :data="chartData" :options="chartOptions" />
            </div>
         </div>

         <!-- Quick Insights -->
         <div class="flex flex-col gap-6">
            <div class="card p-6 md:p-8 border border-outline-subtle bg-gradient-to-b from-surface-card to-surface-low/30 h-full">
               <h3 class="text-xs font-extrabold text-on-surface-muted tracking-widest uppercase mb-6 flex items-center gap-2">
                 <span class="material-symbols-outlined text-[16px] text-amber-500" style="font-variation-settings: 'FILL' 1;">lightbulb</span> 智能洞察
               </h3>
               
               <div class="flex flex-col gap-6">
                 <!-- Insight card 1 -->
                 <div class="flex items-center gap-4 p-4 bg-white rounded-xl border border-outline-subtle shadow-sm hover:-translate-y-1 transition-transform cursor-pointer">
                   <div class="w-12 h-12 bg-gradient-to-br from-accent to-accent-teal/80 rounded-xl flex items-center justify-center text-white shrink-0 shadow-inner">
                     <span class="material-symbols-outlined">menu_book</span>
                   </div>
                   <div class="flex-grow">
                     <div class="flex justify-between items-end mb-1.5">
                       <span class="font-extrabold text-on-surface text-[13px] tracking-wide">哲学类目异动</span>
                       <span class="text-emerald-600 text-[11px] font-bold font-mono">+5%</span>
                     </div>
                     <div class="w-full bg-surface-high rounded-full h-1 overflow-hidden">
                        <div class="bg-accent h-1 rounded-full w-[32%]"></div>
                     </div>
                   </div>
                 </div>

                 <p class="text-[13px] text-on-surface-muted leading-relaxed font-medium">
                   部分关注工程学科的学生小组进入沉浸式阅读的深度学习状态<strong class="text-on-surface font-extrabold">增长了40%</strong>，建议扩大"技术理性"相关采购。
                 </p>
                 <button class="btn-primary py-3 w-full text-sm mt-auto shadow-md shadow-primary/10">一键生成采购草案</button>
               </div>
            </div>
         </div>
      </div>

      <!-- Logs -->
      <div class="card p-6 md:p-8 border border-outline-subtle flex flex-col gap-6 overflow-hidden">
         <div class="flex justify-between items-end border-b border-outline-subtle/50 pb-4">
           <h3 class="text-xl font-bold font-headline flex items-center gap-2 text-on-surface">
              <span class="material-symbols-outlined text-on-surface-muted font-light">memory</span>
              AI 推理审计流水
           </h3>
           <span class="text-[10px] font-extrabold text-accent uppercase tracking-widest flex items-center gap-1.5 bg-accent/5 px-3 py-1 rounded-full border border-accent/10">
             <span class="live-dot bg-accent"></span> 实时诊断中
           </span>
         </div>
         
         <div class="overflow-x-auto no-scrollbar">
            <table class="w-full text-left min-w-[700px]">
               <thead>
                 <tr>
                   <th class="py-3 px-4 bg-surface-low rounded-l-lg text-[11px] font-extrabold uppercase tracking-widest text-on-surface-muted w-1/4">用户查询意图</th>
                   <th class="py-3 px-4 bg-surface-low text-[11px] font-extrabold uppercase tracking-widest text-on-surface-muted w-1/4">RAG 提取关键词</th>
                   <th class="py-3 px-4 bg-surface-low text-[11px] font-extrabold uppercase tracking-widest text-on-surface-muted w-1/3">推荐主题路径</th>
                   <th class="py-3 px-4 bg-surface-low rounded-r-lg text-[11px] font-extrabold uppercase tracking-widest text-on-surface-muted text-right w-1/6">置信度</th>
                 </tr>
               </thead>
               <tbody class="text-sm">
                 <tr v-for="(log, idx) in logs" :key="idx" class="border-b border-outline-subtle/30 hover:bg-surface-low/30 transition-colors group">
                   <td class="py-4 px-4 align-top">
                     <p class="font-extrabold text-on-surface mb-1.5 text-[13px]">{{ log.question }}</p>
                     <p class="text-[10px] text-accent font-bold uppercase tracking-widest bg-accent/5 inline-block px-2 py-0.5 rounded border border-accent/10">意图 | {{ log.intent }}</p>
                   </td>
                   <td class="py-4 px-4 align-top">
                     <div class="flex flex-wrap gap-1.5">
                       <span v-for="tag in log.tags" :key="tag" class="px-2 py-1 bg-surface-high/50 border border-outline-subtle rounded flex items-center gap-1 text-[11px] font-bold text-on-surface-muted group-hover:bg-white group-hover:text-on-surface transition-colors">
                         <span class="material-symbols-outlined text-[10px] opacity-50">tag</span>{{ tag }}
                       </span>
                     </div>
                   </td>
                   <td class="py-4 px-4 align-top">
                     <p class="text-on-surface-muted font-medium mb-2 text-[13px] leading-snug line-clamp-2" :title="log.recommendation">{{ log.recommendation }}</p>
                     <p class="text-[10px] text-emerald-600 font-extrabold font-mono uppercase tracking-widest flex items-center gap-1">
                       <span class="material-symbols-outlined text-[12px]">check_circle</span> 在库命中
                     </p>
                   </td>
                   <td class="py-4 px-4 text-right align-top">
                     <div class="flex flex-col items-end gap-1.5">
                       <span class="font-mono font-extrabold text-on-surface text-[13px]">{{ log.confidence }}</span>
                       <span class="w-16 h-1 bg-surface-high rounded-full overflow-hidden inline-block"><span class="block h-full transition-all duration-1000" :class="parseFloat(log.confidence) > 0.95 ? 'bg-emerald-500' : 'bg-accent'" :style="{ width: `${parseFloat(log.confidence)*100}%` }"></span></span>
                     </div>
                   </td>
                 </tr>
               </tbody>
            </table>
         </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineEmits } from 'vue'
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
import { supabase } from '../supabase.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const emit = defineEmits(['switchToSearch'])

const metrics = ref({
  todaySearches: 0,
  searchGrowth: 12.5,
  conversionRate: 0,
  conversionGrowth: 3.2,
  accuracyRate: 0,
  accuracyGrowth: 1.8
})

const computeRealMetrics = () => {
  const total = parseInt(localStorage.getItem('smartlib_search_count') || '0')
  const converted = parseInt(localStorage.getItem('smartlib_converted_count') || '0')
  metrics.value.accuracyRate = total > 0 ? Math.round((converted / total) * 100) : 0
  metrics.value.conversionRate = total > 0 ? Math.round((converted / total) * 100) : 0
}

const fetchTodaySearches = async () => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const todayStartIso = today.toISOString()
  
  const { count, error } = await supabase
    .from('ai_search_sessions')
    .select('*', { count: 'exact', head: true })
    .gte('created_at', todayStartIso)
  
  if (!error && count !== null) {
    metrics.value.todaySearches = count
  }
}

const chartData = ref({
  labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
  datasets: [
    {
      label: '社会学',
      data: [12, 19, 15, 20, 25, 30, 22],
      backgroundColor: '#8B5CF6',
      borderRadius: 4,
      barThickness: 12
    },
    {
      label: '科幻文学',
      data: [28, 25, 30, 35, 40, 32, 28],
      backgroundColor: '#0D9488',
      borderRadius: 4,
      barThickness: 12
    },
    {
      label: '计算机科学',
      data: [15, 18, 22, 19, 25, 28, 20],
      backgroundColor: '#18181B',
      borderRadius: 4,
      barThickness: 12
    }
  ]
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: '#e4e4e7',
        borderDash: [5, 5]
      },
      border: { display: false }
    },
    x: {
      grid: { display: false },
      border: { display: false }
    }
  },
  plugins: {
    legend: {
      position: 'top',
      align: 'end',
      labels: {
        usePointStyle: true,
        boxWidth: 8,
        boxHeight: 8,
        font: {
          family: "'Manrope', sans-serif",
          weight: 'bold',
          size: 12
        }
      }
    },
    tooltip: {
      backgroundColor: '#18181B',
      titleFont: { family: "'Manrope', sans-serif", size: 13 },
      bodyFont: { family: "'Inter', sans-serif", size: 12 },
      padding: 12,
      cornerRadius: 8
    }
  }
})

const logs = ref([
  {
    question: '想看探讨宇宙社会的科幻书',
    intent: '存在主义探索',
    tags: ['科幻', '宇宙', '社会'],
    recommendation: '推荐《三体》、《三体Ⅱ：黑暗森林》、《三体Ⅲ：死神永生》',
    confidence: '0.98'
  },
  {
    question: '关于人工智能的未来与伦理',
    intent: '技术哲学',
    tags: ['人工智能', '伦理', '未来学'],
    recommendation: '推荐《时间简史》、《未来简史》',
    confidence: '0.95'
  },
  {
    question: '现代都市人的心理困境',
    intent: '心理学分析',
    tags: ['心理学', '现代病', '焦虑'],
    recommendation: '推荐《单向度的人》、《倦怠社会》',
    confidence: '0.92'
  },
  {
    question: '如何理解后现代主义建筑',
    intent: '艺术流派科普',
    tags: ['建筑学', '后现代', '美学'],
    recommendation: '推荐《走向新建筑》、《空间的生产》',
    confidence: '0.89'
  }
])

onMounted(() => {
  fetchTodaySearches()
  computeRealMetrics()
  setInterval(fetchTodaySearches, 30000)
})
</script>