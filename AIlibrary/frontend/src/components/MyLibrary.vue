<template>
  <div class="bg-[#FAFAFA] font-body text-brand-night antialiased min-h-screen pb-12">
    <div v-if="showToast" class="fixed top-24 left-1/2 -translate-x-1/2 z-[100] bg-brand-night text-white px-6 py-3 rounded-full flex items-center gap-3 shadow-xl animate-fade-up">
      <span class="material-symbols-outlined text-brand-aurora_start">info</span>
      <span class="text-sm font-bold">{{ toastMessage }}</span>
      <button @click="showToast = false" class="ml-2 hover:text-gray-300">
        <span class="material-symbols-outlined text-sm">close</span>
      </button>
    </div>

    <header class="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-6 py-4 bg-[#F7F7F7] bg-opacity-90 backdrop-blur-md border-b border-gray-200 dark:border-gray-800 font-sans antialiased transition-all">
      <div class="flex items-center gap-8">
        <span class="text-xl font-bold tracking-tighter text-black dark:text-white cursor-pointer hover:opacity-80 transition-opacity" @click="$emit('switchToSearch')">SmartLib AI</span>
        <nav class="hidden md:flex gap-6">
          <a @click.prevent="topNav = 'library'" :class="[topNav === 'library' ? 'text-black dark:text-white border-b-2 border-black dark:border-white pb-1' : 'text-gray-500 dark:text-gray-400 hover:text-black dark:hover:text-white', 'transition-colors duration-200 ease-in-out cursor-pointer']" href="#">我的书库</a>
          <a @click.prevent="showAllLoans = true" :class="[topNav === 'history' ? 'text-black border-b-2 border-black pb-1' : 'text-gray-500 hover:text-black', 'transition-colors duration-200 ease-in-out cursor-pointer']" href="#">借阅记录</a>
          <a @click.prevent="showNotification('正在获取阅读统计...')" class="text-gray-500 hover:text-black transition-colors duration-200 ease-in-out cursor-pointer" href="#">阅读统计</a>
          <a @click.prevent="showNotification('AI 路径生成中，请稍候')" class="text-gray-500 hover:text-black transition-colors duration-200 ease-in-out cursor-pointer" href="#">AI路径</a>
        </nav>
      </div>
      <div class="flex items-center gap-4">
        <div class="relative hidden sm:block group">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm transition-colors group-focus-within:text-brand-aurora_start">search</span>
          <input v-model="searchQuery" class="pl-10 pr-10 py-1.5 rounded-full border border-transparent bg-white text-sm focus:ring-2 focus:ring-brand-aurora_start/20 focus:border-brand-aurora_start/30 w-64 shadow-sm transition-all" placeholder="搜索书名或AI建议..." type="text"/>
          <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
            <span class="material-symbols-outlined text-sm">close</span>
          </button>
        </div>
        <button @click="showNotification('暂无新通知')" class="text-black dark:text-white hover:bg-gray-200 p-1.5 rounded-full transition-colors"><span class="material-symbols-outlined hover:scale-110 transition-transform">notifications</span></button>
        <button @click="$emit('switchToSearch')" class="text-black hover:bg-gray-200 p-1.5 rounded-full transition-colors hidden sm:block" title="返回发现页"><span class="material-symbols-outlined hover:scale-110 transition-transform">explore</span></button>
        <button @click="showNotification('打开全局设置')" class="text-black dark:text-white hover:bg-gray-200 p-1.5 rounded-full transition-colors"><span class="material-symbols-outlined hover:rotate-90 transition-transform">settings</span></button>
        <div v-if="currentUser" class="flex items-center gap-3">
          <div class="text-right hidden sm:block">
            <p class="text-sm font-bold">{{ currentUser.username }}</p>
            <p class="text-xs text-gray-400">{{ currentUser.email }}</p>
          </div>
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-brand-aurora_start to-brand-aurora_end flex items-center justify-center text-white font-bold">
            {{ currentUser.username?.charAt(0).toUpperCase() }}
          </div>
        </div>
      </div>
    </header>

    <div class="flex pt-16 min-h-screen font-['Public_Sans',sans-serif]">
      <aside class="hidden md:flex flex-col fixed left-0 top-0 h-full p-4 w-64 border-r border-gray-100 bg-[#F7F7F7] pt-20 z-40 text-sm font-medium">
        <div class="mb-8 px-4">
          <div class="flex items-center gap-3 mb-1">
            <span class="font-black tracking-tight text-xl bg-clip-text text-transparent bg-gradient-to-r from-brand-aurora_start to-brand-aurora_end">SmartLib AI</span>
          </div>
          <p class="text-xs text-gray-400 relative">个人专业书库 <span class="absolute top-1 right-20 w-1.5 h-1.5 bg-green-500 rounded-full animate-ping"></span><span class="absolute top-1 right-20 w-1.5 h-1.5 bg-green-500 rounded-full"></span></p>
        </div>
        <div class="flex flex-col gap-2">
          <a @click.prevent="sideNav = 'overview'" :class="[sideNav === 'overview' ? 'bg-gray-100 text-black rounded-lg' : 'text-gray-400 hover:bg-gray-50', 'flex items-center gap-3 px-4 py-2 transition-all duration-300 cursor-pointer']" href="#">
            <span class="material-symbols-outlined" :style="sideNav === 'overview' ? 'font-variation-settings: \'FILL\' 1;' : ''">dashboard</span>
            <span>总览</span>
          </a>
          <a @click.prevent="sideNav = 'books'" :class="[sideNav === 'books' ? 'bg-gray-100 text-black rounded-lg' : 'text-gray-400 hover:bg-gray-50', 'flex items-center gap-3 px-4 py-2 transition-all duration-300 cursor-pointer']" href="#">
            <span class="material-symbols-outlined" :style="sideNav === 'books' ? 'font-variation-settings: \'FILL\' 1;' : ''">menu_book</span>
            <span>书籍</span>
          </a>
          <a @click.prevent="sideNav = 'stats'" :class="[sideNav === 'stats' ? 'bg-gray-100 text-black rounded-lg' : 'text-gray-400 hover:bg-gray-50', 'flex items-center gap-3 px-4 py-2 transition-all duration-300 cursor-pointer']" href="#">
            <span class="material-symbols-outlined" :style="sideNav === 'stats' ? 'font-variation-settings: \'FILL\' 1;' : ''">leaderboard</span>
            <span>统计</span>
          </a>
          <a @click.prevent="sideNav = 'ai'" :class="[sideNav === 'ai' ? 'bg-gray-100 text-black rounded-lg' : 'text-gray-400 hover:bg-gray-50', 'flex items-center gap-3 px-4 py-2 transition-all duration-300 cursor-pointer']" href="#">
            <span class="material-symbols-outlined" :style="sideNav === 'ai' ? 'font-variation-settings: \'FILL\' 1;' : ''">psychology</span>
            <span>AI助手</span>
          </a>
          <a @click.prevent="sideNav = 'settings'" :class="[sideNav === 'settings' ? 'bg-gray-100 text-black rounded-lg' : 'text-gray-400 hover:bg-gray-50', 'flex items-center gap-3 px-4 py-2 transition-all duration-300 cursor-pointer mt-4']" href="#">
            <span class="material-symbols-outlined" :style="sideNav === 'settings' ? 'font-variation-settings: \'FILL\' 1;' : ''">settings</span>
            <span>设置</span>
          </a>
        </div>
        <div class="mt-auto p-4 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow cursor-crosshair group">
          <h4 class="text-xs font-bold mb-3 uppercase tracking-wider text-gray-400 group-hover:text-brand-night transition-colors">阅读偏好雷达</h4>
          <div class="aspect-square relative flex items-center justify-center">
            <div class="absolute inset-0 flex items-center justify-center">
              <svg class="w-full h-full opacity-20" viewBox="0 0 100 100">
                <polygon fill="none" points="50,10 90,40 75,90 25,90 10,40" stroke="currentColor" stroke-width="0.5"></polygon>
                <polygon fill="none" points="50,25 75,45 65,75 35,75 25,45" stroke="currentColor" stroke-width="0.5"></polygon>
              </svg>
              <svg class="w-full h-full absolute transition-all duration-700 group-hover:scale-105 origin-center" viewBox="0 0 100 100">
                <polygon fill="#18181B" fill-opacity="0.1" points="50,20 85,45 70,80 30,70 20,35" stroke="#18181B" stroke-width="1.5" class="group-hover:fill-brand-aurora_start/20 group-hover:stroke-brand-aurora_start transition-colors duration-500"></polygon>
              </svg>
            </div>
            <div class="absolute -top-1 text-[10px] font-bold">社会学</div>
            <div class="absolute top-1/2 -right-2 -translate-y-1/2 text-[10px] font-bold rotate-90">硬核科学</div>
            <div class="absolute -bottom-1 text-[10px] font-bold">文学</div>
          </div>
          <p class="text-[10px] text-center mt-4 text-gray-500 italic">"您的硬核科学探索已超过 82% 用户"</p>
        </div>
      </aside>

      <!-- 总览 Tab -->
      <main v-if="sideNav === 'overview'" class="flex-1 md:ml-64 p-8 w-full max-w-[1200px] mx-auto transition-opacity duration-300">
        <header class="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 class="text-4xl font-black tracking-tight mb-2">书库总览</h1>
            <p class="text-gray-500">欢迎回来，书库共收录 {{ libraryBooks.length }} 本图书。</p>
          </div>
          <button @click="$emit('switchToSearch')" class="px-5 py-2.5 bg-white border border-gray-200 text-brand-night text-sm font-bold rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center gap-2 self-start">
            <span class="material-symbols-outlined text-[18px]">arrow_back</span>
            返回发现中心
          </button>
        </header>

        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 rounded-xl bg-brand-aurora_start/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-brand-aurora_start">menu_book</span>
              </div>
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">总藏书</span>
            </div>
            <p class="text-4xl font-black">{{ libraryBooks.length }}</p>
          </div>
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center">
                <span class="material-symbols-outlined text-emerald-600">calendar_today</span>
              </div>
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">本月新增</span>
            </div>
            <p class="text-4xl font-black">{{ recentMonthCount }}</p>
          </div>
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center">
                <span class="material-symbols-outlined text-amber-600">tag</span>
              </div>
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">最常标签</span>
            </div>
            <p class="text-2xl font-black">{{ topTag || '--' }}</p>
          </div>
        </div>

        <!-- 最近加入 -->
        <section class="mb-10">
          <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
            <span class="material-symbols-outlined text-brand-night">schedule</span> 最近加入
          </h2>
          <div v-if="libraryBooks.length === 0" class="bg-white rounded-xl p-12 text-center">
            <span class="material-symbols-outlined text-6xl text-gray-200 mb-4">menu_book</span>
            <p class="text-gray-500 mb-4">您的书库还是空的</p>
            <button @click="$emit('switchToSearch')" class="px-6 py-2 bg-brand-aurora_start text-white font-bold rounded-lg hover:bg-brand-aurora_end transition-all">去发现书籍</button>
          </div>
          <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div v-for="book in libraryBooks.slice(0, 3)" :key="book.id" class="bg-white p-4 rounded-xl border border-gray-100 flex gap-3 hover:shadow-md transition-shadow">
              <div class="w-14 h-20 flex-shrink-0 bg-gray-100 rounded-lg overflow-hidden">
                <img class="w-full h-full object-cover" :src="getBookCover(book.title, [])" />
              </div>
              <div class="flex flex-col justify-center min-w-0">
                <h3 class="font-bold text-sm truncate">{{ book.title }}</h3>
                <p class="text-xs text-gray-400">{{ book.author }}</p>
                <span class="text-[10px] font-bold mt-1" :class="book.status === '在馆' ? 'text-emerald-600' : 'text-rose-600'">{{ book.status }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 标签分布 -->
        <section>
          <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
            <span class="material-symbols-outlined text-brand-night">label</span> 标签分布
          </h2>
          <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <div v-if="tagEntries.length === 0" class="text-center py-8 text-gray-400">
              <span class="material-symbols-outlined text-4xl mb-2">tag</span>
              <p>加入书籍后这里会显示标签分布</p>
            </div>
            <div v-else class="space-y-4">
              <div v-for="[tag, count] in tagEntries.slice(0, 5)" :key="tag" class="flex items-center gap-3">
                <span class="text-sm font-bold w-16 text-right shrink-0">{{ tag }}</span>
                <div class="flex-1 bg-gray-100 rounded-full h-5 overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-brand-aurora_start to-brand-aurora_end rounded-full transition-all duration-700" :style="{ width: (count / tagMaxCount * 100) + '%' }"></div>
                </div>
                <span class="text-xs font-bold text-gray-500 w-6">{{ count }}</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      <!-- 书籍 Tab -->
      <main v-if="sideNav === 'books'" class="flex-1 md:ml-64 p-8 w-full max-w-[1200px] mx-auto transition-opacity duration-300">
        <header class="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 class="text-4xl font-black tracking-tight mb-2">我的书库</h1>
            <p class="text-gray-500">共 {{ libraryBooks.length }} 本藏书</p>
          </div>
          <button @click="$emit('switchToSearch')" class="px-5 py-2.5 bg-white border border-gray-200 text-brand-night text-sm font-bold rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center gap-2 self-start">
            <span class="material-symbols-outlined text-[18px]">arrow_back</span>
            返回发现中心
          </button>
        </header>

        <div v-if="libraryBooks.length === 0" class="bg-white rounded-xl p-12 text-center">
          <span class="material-symbols-outlined text-6xl text-gray-200 mb-4">menu_book</span>
          <p class="text-gray-500 mb-4">您的书库还是空的</p>
          <button @click="$emit('switchToSearch')" class="px-6 py-2 bg-brand-aurora_start text-white font-bold rounded-lg hover:bg-brand-aurora_end transition-all">去发现书籍</button>
        </div>

        <div v-else class="space-y-4">
          <div v-for="book in libraryBooks" :key="book.id" class="bg-white rounded-xl p-4 flex items-center gap-4 hover:bg-gray-50 transition-colors border border-gray-100">
            <div class="w-16 h-24 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
              <img :src="getBookCover(book.title, [])" :alt="book.title" class="w-full h-full object-cover" />
            </div>
            <div class="flex-1">
              <h3 class="font-bold text-lg">{{ book.title }}</h3>
              <p class="text-sm text-gray-500">{{ book.author }}</p>
              <div class="flex items-center gap-2 mt-2">
                <span class="text-xs font-bold px-2 py-0.5 rounded" :class="book.status === '在馆' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">{{ book.status }}</span>
                <span class="text-xs text-gray-400">索书号: {{ book.call_number || 'N/A' }}</span>
              </div>
            </div>
            <div class="flex flex-col items-end gap-2">
              <p class="text-xs text-gray-400">{{ new Date(book.created_at).toLocaleDateString('zh-CN') }}</p>
              <div class="flex gap-2">
                <button @click="openComments(book)" class="flex items-center gap-1 text-sm text-brand-aurora_start hover:text-brand-aurora_end transition-colors bg-white border border-brand-aurora_start/30 px-3 py-1.5 rounded-lg hover:bg-brand-aurora_start/5">
                  <span class="material-symbols-outlined text-xs">comment</span>
                  留言 ({{ getCommentCount(book.title) }})
                </button>
                <button @click="returnBook(book)" class="px-3 py-1.5 bg-red-500 hover:bg-red-600 text-white text-sm font-bold rounded-lg transition-colors">归还</button>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 统计 Tab -->
      <main v-if="sideNav === 'stats'" class="flex-1 md:ml-64 p-8 w-full max-w-[1200px] mx-auto transition-opacity duration-300">
        <header class="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 class="text-4xl font-black tracking-tight mb-2">阅读统计</h1>
            <p class="text-gray-500">基于您的书库数据分析</p>
          </div>
          <button @click="$emit('switchToSearch')" class="px-5 py-2.5 bg-white border border-gray-200 text-brand-night text-sm font-bold rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center gap-2 self-start">
            <span class="material-symbols-outlined text-[18px]">arrow_back</span>
            返回发现中心
          </button>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- 标签分布图 -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <h2 class="text-lg font-bold mb-6 flex items-center gap-2">
              <span class="material-symbols-outlined text-brand-aurora_start">pie_chart</span> 标签分布
            </h2>
            <div v-if="tagEntries.length === 0" class="text-center py-12 text-gray-400">
              <span class="material-symbols-outlined text-4xl mb-2">bar_chart</span>
              <p>加入书籍后这里会显示统计图表</p>
            </div>
            <div v-else class="space-y-3">
              <div v-for="[tag, count] in tagEntries.slice(0, 8)" :key="tag" class="flex items-center gap-3">
                <span class="text-xs font-bold w-14 text-right shrink-0 text-gray-600">{{ tag }}</span>
                <div class="flex-1 bg-gray-100 rounded-full h-6 overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-[#8B5CF6] to-[#0D9488] rounded-full transition-all duration-700 flex items-center justify-end pr-2" :style="{ width: (count / tagMaxCount * 100) + '%' }">
                    <span v-if="count / tagMaxCount > 0.3" class="text-[10px] font-bold text-white">{{ count }}</span>
                  </div>
                </div>
                <span v-if="count / tagMaxCount <= 0.3" class="text-xs font-bold text-gray-500">{{ count }}</span>
              </div>
            </div>
          </div>

          <!-- 时间线 -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <h2 class="text-lg font-bold mb-6 flex items-center gap-2">
              <span class="material-symbols-outlined text-brand-aurora_start">timeline</span> 加入时间线
            </h2>
            <div v-if="libraryBooks.length === 0" class="text-center py-12 text-gray-400">
              <span class="material-symbols-outlined text-4xl mb-2">timeline</span>
              <p>暂无数据</p>
            </div>
            <div v-else class="space-y-6 relative">
              <div class="absolute left-4 top-0 bottom-0 w-px bg-gray-200"></div>
              <div v-for="book in libraryBooks.slice(0, 6)" :key="book.id" class="flex gap-4 items-start relative">
                <div class="w-8 h-8 rounded-full bg-brand-aurora_start/10 border-2 border-brand-aurora_start flex items-center justify-center shrink-0 z-10">
                  <span class="material-symbols-outlined text-brand-aurora_start text-sm">menu_book</span>
                </div>
                <div class="flex-1 pb-2">
                  <p class="font-bold text-sm">{{ book.title }}</p>
                  <p class="text-xs text-gray-400">{{ book.author }} · {{ new Date(book.created_at).toLocaleDateString('zh-CN') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- AI助手 / 设置 占位 -->
      <main v-if="sideNav === 'ai' || sideNav === 'settings'" class="flex-1 md:ml-64 p-8 w-full max-w-[1200px] mx-auto transition-opacity duration-300">
        <div class="bg-white rounded-2xl p-16 text-center border border-gray-100">
          <span class="material-symbols-outlined text-7xl text-gray-200 mb-6">{{ sideNav === 'ai' ? 'psychology' : 'settings' }}</span>
          <h2 class="text-2xl font-black mb-2">{{ sideNav === 'ai' ? 'AI 助手' : '设置' }}</h2>
          <p class="text-gray-500">功能开发中，敬请期待</p>
        </div>
      </main>
    </div>

    <div v-if="showAllLoans" class="fixed inset-0 z-[200] bg-black/50 backdrop-blur-sm flex items-center justify-center p-4" @click.self="showAllLoans = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden animate-[fadeUp_0.3s_ease-out]">
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 class="text-xl font-bold flex items-center gap-2">
            <span class="material-symbols-outlined text-brand-night">history</span>
            借阅记录
          </h2>
          <button @click="showAllLoans = false" class="text-gray-400 hover:text-black p-2 rounded-full hover:bg-gray-100 transition-colors">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-[60vh]">
          <div v-if="libraryBooks.length === 0" class="text-center py-12">
            <span class="material-symbols-outlined text-6xl text-gray-200 mb-4">bookmark_border</span>
            <p class="text-gray-500">暂无借阅记录</p>
            <p class="text-sm text-gray-400 mt-2">在发现页搜索书籍并加入书库</p>
          </div>
          
          <div v-else class="space-y-4">
            <div v-for="book in libraryBooks" :key="book.id" class="bg-gray-50 rounded-xl p-4 flex items-center gap-4 hover:bg-gray-100 transition-colors">
              <div class="w-16 h-24 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                <img :src="book.cover_url" :alt="book.title" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1">
                <h3 class="font-bold text-lg">{{ book.title }}</h3>
                <p class="text-sm text-gray-500">{{ book.author }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <span class="text-xs font-bold px-2 py-0.5 rounded" :class="book.status === '在馆' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                    {{ book.status }}
                  </span>
                  <span class="text-xs text-gray-400">索书号: {{ book.call_number || 'N/A' }}</span>
                </div>
              </div>
              <div class="flex flex-col items-end gap-2">
                <p class="text-xs text-gray-400">{{ new Date(book.created_at).toLocaleDateString('zh-CN') }}</p>
                <div class="flex gap-2">
                  <button 
                    @click="openComments(book)" 
                    class="flex items-center gap-1 text-sm text-brand-aurora_start hover:text-brand-aurora_end transition-colors bg-white border border-brand-aurora_start/30 px-3 py-1.5 rounded-lg hover:bg-brand-aurora_start/5"
                  >
                    <span class="material-symbols-outlined text-xs">comment</span>
                    留言 ({{ getCommentCount(book.title) }})
                  </button>
                  <button 
                    @click="returnBook(book)" 
                    class="px-3 py-1.5 bg-red-500 hover:bg-red-600 text-white text-sm font-bold rounded-lg transition-colors"
                  >
                    归还
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showCommentsModal" class="fixed inset-0 z-[300] bg-black/50 backdrop-blur-sm flex items-center justify-center p-4" @click.self="showCommentsModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[80vh] overflow-hidden animate-[fadeUp_0.3s_ease-out]">
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-14 bg-gray-200 rounded-lg overflow-hidden">
              <img v-if="currentBook" :src="currentBook.cover_url" :alt="currentBook.title" class="w-full h-full object-cover" />
            </div>
            <div>
              <h2 class="text-lg font-bold">{{ currentBook?.title }}</h2>
              <p class="text-sm text-gray-500">{{ comments.length }} 条留言</p>
            </div>
          </div>
          <button @click="showCommentsModal = false" class="text-gray-400 hover:text-black p-2 rounded-full hover:bg-gray-100 transition-colors">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        
        <div class="p-4 overflow-y-auto max-h-[45vh] space-y-4">
          <div v-if="comments.length === 0" class="text-center py-8">
            <span class="material-symbols-outlined text-4xl text-gray-200 mb-2">message</span>
            <p class="text-gray-500 text-sm">暂无留言，快来发表第一条留言吧！</p>
          </div>
          
          <div v-for="comment in comments" :key="comment.id" class="bg-gray-50 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-brand-aurora_start to-brand-aurora_end flex items-center justify-center text-white text-sm font-bold">
                  {{ comment.user_name?.charAt(0) || '匿' }}
                </div>
                <div>
                  <p class="text-sm font-bold">{{ comment.user_name || '匿名用户' }}</p>
                  <p class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</p>
                </div>
              </div>
              <div class="flex items-center gap-0.5">
                <span v-for="i in 5" :key="i" class="material-symbols-outlined text-xs" :class="i <= (comment.rating || 5) ? 'text-amber-400' : 'text-gray-300'" style="font-variation-settings: 'FILL' 1;">star</span>
              </div>
            </div>
            <p class="text-sm text-gray-700">{{ comment.content }}</p>
          </div>
        </div>
        
        <div class="p-4 border-t border-gray-100">
          <div class="flex gap-2 mb-3">
            <span class="text-xs text-gray-500">评分：</span>
            <button 
              v-for="i in 5" 
              :key="i" 
              @click="newCommentRating = i"
              class="material-symbols-outlined transition-transform hover:scale-110"
              :class="i <= newCommentRating ? 'text-amber-400' : 'text-gray-300'"
              style="font-variation-settings: 'FILL' 1; font-size: 18px;"
            >star</button>
          </div>
          <input 
            v-model="newCommentName" 
            placeholder="您的昵称（可选）" 
            class="w-full px-4 py-2 mb-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-brand-aurora_start/20 focus:border-brand-aurora_start/30 outline-none"
          />
          <textarea 
            v-model="newCommentContent" 
            placeholder="写下您的留言..." 
            class="w-full px-4 py-3 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-brand-aurora_start/20 focus:border-brand-aurora_start/30 outline-none resize-none"
            rows="2"
          ></textarea>
          <button 
            @click="submitComment" 
            :disabled="!newCommentContent.trim()"
            class="w-full mt-3 py-2.5 bg-brand-night text-white text-sm font-bold rounded-lg hover:bg-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            发表留言
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits, onMounted, watch } from 'vue'
import { supabase } from '../supabase.js'
import { getBookCover } from '../coverUtils.js'

const props = defineProps({
  currentUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['switchToSearch'])

const topNav = ref('library')
const sideNav = ref('overview')
const searchQuery = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const showAllLoans = ref(false)
const libraryBooks = ref([])
const comments = ref([])
const showCommentsModal = ref(false)
const currentBook = ref(null)
const newCommentName = ref('')
const newCommentContent = ref('')
const newCommentRating = ref(5)

// 总览 & 统计 Tab 计算属性
const recentMonthCount = computed(() => {
  const now = new Date()
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
  return libraryBooks.value.filter(b => new Date(b.created_at) >= monthStart).length
})

const tagEntries = computed(() => {
  const counts = {}
  // 从 book_comments 或 tags 聚合标签（简化：从书名推断或默认）
  // 实际标签数据存储在雷达的 libraryTagCounts 中，这里从 localStorage 读取
  try {
    // 从 localStorage 读取上次从 App.vue 传来的标签计数
    // 由于跨组件通信，这里用简单的静态聚合
  } catch {}
  // 暂时用固定标签展示（后续可扩展）
  if (libraryBooks.value.length === 0) return []
  // 简单聚合：从书名关键词推断
  const tagMap = {}
  for (const book of libraryBooks.value) {
    const title = book.title || ''
    const author = book.author || ''
    if (title.includes('三体') || title.includes('科幻')) tagMap['科幻'] = (tagMap['科幻'] || 0) + 1
    else if (title.includes('Python') || title.includes('编程') || title.includes('代码')) tagMap['编程'] = (tagMap['编程'] || 0) + 1
    else if (title.includes('经济') || title.includes('商业')) tagMap['经济'] = (tagMap['经济'] || 0) + 1
    else if (title.includes('心理') || title.includes('焦虑')) tagMap['心理'] = (tagMap['心理'] || 0) + 1
    else if (title.includes('文学') || title.includes('小说') || title.includes('百年孤独') || title.includes('活着')) tagMap['文学'] = (tagMap['文学'] || 0) + 1
    else if (title.includes('历史') || title.includes('文明')) tagMap['历史'] = (tagMap['历史'] || 0) + 1
    else if (title.includes('哲学') || title.includes('思想')) tagMap['哲学'] = (tagMap['哲学'] || 0) + 1
    else tagMap['其他'] = (tagMap['其他'] || 0) + 1
  }
  return Object.entries(tagMap).sort((a, b) => b[1] - a[1])
})

const tagMaxCount = computed(() => {
  const entries = tagEntries.value
  return entries.length > 0 ? entries[0][1] : 1
})

const topTag = computed(() => {
  const entries = tagEntries.value
  return entries.length > 0 ? entries[0][0] : ''
})

const fetchLibraryBooks = async () => {
  if (!props.currentUser) {
    libraryBooks.value = []
    return
  }
  
  const { data, error } = await supabase
    .from('library_books')
    .select('*')
    .eq('user_id', props.currentUser.id)
    .order('created_at', { ascending: false })
  
  if (!error && data) {
    libraryBooks.value = data
  } else {
    libraryBooks.value = []
  }
}

const fetchComments = async (bookTitle) => {
  const { data, error } = await supabase
    .from('book_comments')
    .select('*')
    .eq('book_title', bookTitle)
    .order('created_at', { ascending: false })
  
  if (!error && data) {
    comments.value = data
  } else {
    comments.value = []
  }
}

const getCommentCount = (bookTitle) => {
  return comments.value.filter(c => c.book_title === bookTitle).length
}

const openComments = async (book) => {
  currentBook.value = book
  await fetchComments(book.title)
  showCommentsModal.value = true
  newCommentName.value = ''
  newCommentContent.value = ''
  newCommentRating.value = 5
}

const submitComment = async () => {
  if (!newCommentContent.value.trim()) return
  
  const { error } = await supabase
    .from('book_comments')
    .insert([{
      book_title: currentBook.value.title,
      book_author: currentBook.value.author,
      user_name: newCommentName.value || '匿名用户',
      content: newCommentContent.value,
      rating: newCommentRating.value,
      user_id: props.currentUser?.id ? String(props.currentUser.id) : null
    }])
  
  if (error) {
    console.error('发表留言失败:', error)
    showNotification('发表留言失败：' + error.message)
  } else {
    showCommentsModal.value = false
    showNotification('感谢你的留言！')
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const returnBook = async (book) => {
  if (!confirm(`确定要归还《${book.title}》吗？`)) return
  
  const { error } = await supabase
    .from('library_books')
    .delete()
    .eq('id', book.id)
  
  if (error) {
    console.error('归还失败:', error)
    showNotification('归还失败：' + error.message)
  } else {
    showNotification('已成功归还：' + book.title)
    await fetchLibraryBooks()
  }
}

const showNotification = (msg) => {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

watch(() => props.currentUser, () => {
  fetchLibraryBooks()
}, { immediate: true })

onMounted(() => {
  fetchLibraryBooks()
})
</script>

<style scoped>
@keyframes fadeUp {
  0% { opacity: 0; transform: translateY(10px) translateX(-50%); }
  100% { opacity: 1; transform: translateY(0) translateX(-50%); }
}

.animate-fade-up {
  animation: fadeUp 0.3s ease-out forwards;
}
</style>