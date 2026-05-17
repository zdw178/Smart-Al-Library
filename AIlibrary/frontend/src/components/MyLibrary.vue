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

      <main class="flex-1 md:ml-64 p-8 w-full max-w-[1200px] mx-auto transition-opacity duration-300">
        <header class="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 class="text-4xl font-black tracking-tight mb-2">我的书库</h1>
            <p class="text-gray-500">欢迎回来，今日已深度阅读 45 分钟。</p>
          </div>
          <button @click="$emit('switchToSearch')" class="px-5 py-2.5 bg-white border border-gray-200 text-brand-night text-sm font-bold rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center gap-2 self-start">
            <span class="material-symbols-outlined text-[18px]">arrow_back</span>
            返回发现中心
          </button>
        </header>

        <div class="grid grid-cols-12 gap-6">
          <section class="col-span-12 lg:col-span-8">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold flex items-center gap-2">
                <span class="material-symbols-outlined text-brand-night">bookmark</span>
                当前借阅
              </h2>
              <span @click="showAllLoans = true" class="text-sm font-medium text-gray-400 hover:text-brand-night cursor-pointer transition-colors">查看全部 <span class="material-symbols-outlined text-xs align-middle">chevron_right</span></span>
            </div>
            
            <div v-if="libraryBooks.length === 0" class="bg-white rounded-xl p-12 text-center">
              <span class="material-symbols-outlined text-6xl text-gray-200 mb-4">menu_book</span>
              <p class="text-gray-500 mb-4">您的书库还是空的</p>
              <button @click="$emit('switchToSearch')" class="px-6 py-2 bg-brand-aurora_start text-white font-bold rounded-lg hover:bg-brand-aurora_end transition-all">
                去发现书籍
              </button>
            </div>
            
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="book in libraryBooks.slice(0, 4)" :key="book.id" class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex gap-4 hover:shadow-md transition-shadow group relative overflow-hidden">
                <div class="w-24 h-36 flex-shrink-0 bg-gray-200 rounded shadow-md overflow-hidden cursor-pointer">
                  <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" :src="book.cover_url" />
                </div>
                <div class="flex-1 flex flex-col">
                  <h3 class="font-bold text-lg leading-tight mb-1 cursor-pointer hover:text-brand-aurora_start transition-colors">{{ book.title }}</h3>
                  <p class="text-xs text-gray-500 mb-4">{{ book.author }}</p>
                  <div class="mt-auto">
                    <div class="flex justify-between text-[10px] font-bold mb-1">
                      <span>{{ book.status }}</span>
                    </div>
                    <div class="mt-3 flex gap-2">
                       <button class="flex-1 bg-brand-night text-white text-[10px] font-bold py-1.5 rounded hover:bg-black transition-colors">查看详情</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="col-span-12 lg:col-span-4">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold flex items-center gap-2">
                <span class="material-symbols-outlined text-brand-night">favorite</span>
                我的收藏
              </h2>
            </div>
            <div class="space-y-4">
              <div v-for="book in libraryBooks.slice(0, 2)" :key="book.id" @click="showNotification('打开《' + book.title + '》详情页')" class="bg-white p-4 rounded-xl border border-gray-100 flex items-center gap-4 group cursor-pointer hover:border-brand-aurora_start/40 hover:shadow-sm transition-all transform hover:-translate-y-0.5">
                <div class="w-10 h-14 bg-gray-50 rounded flex-shrink-0 overflow-hidden shadow-sm">
                  <img class="w-full h-full object-cover" :src="book.cover_url" />
                </div>
                <div>
                  <h4 class="font-bold text-sm group-hover:text-brand-aurora_start transition-colors">{{ book.title }}</h4>
                  <p class="text-[10px] text-gray-400">{{ book.author }}</p>
                </div>
                <span class="material-symbols-outlined ml-auto text-gray-300 group-hover:text-brand-aurora_start transition-colors">arrow_forward_ios</span>
              </div>
            </div>
          </section>

          <section class="col-span-12 mt-4">
            <div class="aurora-border p-[1px] relative rounded-[0.8rem] overflow-hidden group">
              <div class="absolute inset-0 bg-gradient-to-r from-[#8B5CF6] to-[#0D9488] opacity-100 group-hover:opacity-100 blur-[2px] transition-opacity duration-1000 -z-10"></div>
              
              <div class="bg-white rounded-[0.75rem] p-8 relative z-10 m-[1px]">
                <div class="flex items-center justify-between mb-8">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-full bg-gradient-to-br from-brand-aurora_start to-brand-aurora_end flex items-center justify-center text-white shadow-md shadow-brand-aurora_start/20">
                      <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">psychology</span>
                    </div>
                    <div>
                      <h2 class="text-2xl font-black tracking-tight">AI 学习路径</h2>
                      <p class="text-sm text-gray-500">基于您的阅读历史的深度进阶建议</p>
                    </div>
                  </div>
                  <button @click="showNotification('编辑学习路径设定')" class="text-gray-400 hover:text-brand-night bg-gray-50 hover:bg-gray-100 p-2 rounded-full transition-colors flex items-center gap-2 text-xs font-bold px-4"><span class="material-symbols-outlined text-[16px]">tune</span> 定制</button>
                </div>
                
                <div class="relative">
                  <div class="absolute left-6 top-0 bottom-0 w-px bg-gradient-to-b from-brand-aurora_start via-brand-aurora_end to-transparent"></div>
                  
                  <div class="space-y-12 relative">
                    <div class="flex gap-12 items-start group/milestone cursor-pointer" @click="showNotification('回顾：认知革命的学习笔记')">
                      <div class="z-10 w-12 h-12 rounded-full bg-brand-aurora_start/10 border-2 border-brand-aurora_start flex items-center justify-center shadow-sm transition-transform group-hover/milestone:scale-110">
                        <span class="material-symbols-outlined text-brand-aurora_start" style="font-variation-settings: 'FILL' 1;">check_circle</span>
                      </div>
                      <div class="flex-1 bg-transparent group-hover/milestone:bg-brand-aurora_start/5 -my-4 p-4 rounded-xl transition-colors">
                        <div class="flex items-center gap-3 mb-2">
                          <span class="px-2 py-0.5 rounded bg-brand-aurora_start/10 text-brand-aurora_start text-[10px] font-black uppercase tracking-widest">已掌握</span>
                          <h3 class="font-bold text-lg group-hover/milestone:text-brand-aurora_start transition-colors">认知革命：从生物学到历史学</h3>
                        </div>
                        <p class="text-sm text-gray-600 max-w-2xl">探索虚构故事如何让数万智人进行灵活合作。结合此前阅读的《枪炮、病菌与钢铁》的前三章。</p>
                      </div>
                    </div>

                    <div class="flex gap-12 items-start group/milestone opacity-50 hover:opacity-80 transition-opacity cursor-not-allowed">
                      <div class="z-10 w-12 h-12 rounded-full bg-gray-50 border-2 border-gray-200 flex items-center justify-center shadow-sm">
                        <span class="material-symbols-outlined text-gray-400">lock</span>
                      </div>
                      <div class="flex-1">
                        <div class="flex items-center gap-3 mb-2">
                          <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-400 text-[10px] font-black uppercase tracking-widest">待解锁</span>
                          <h3 class="font-bold text-lg">完成更多阅读解锁</h3>
                        </div>
                        <p class="text-sm text-gray-600 max-w-2xl">继续在发现页搜索和借阅书籍，解锁更多个性化学习路径。</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
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
import { ref, defineEmits, onMounted, watch } from 'vue'
import { supabase } from '../supabase.js'

const props = defineProps({
  currentUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['switchToSearch'])

const topNav = ref('library')
const sideNav = ref('books')
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