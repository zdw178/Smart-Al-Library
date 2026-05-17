<template>
  <div class="card group flex flex-col h-full overflow-hidden" :class="{'md:flex-row p-0 md:p-0': featured, 'p-0': !featured}">
    <div 
      class="overflow-hidden bg-surface-low transition-transform duration-700 group-hover:scale-[1.02] relative"
      :class="{'w-full md:w-2/5 aspect-[3/4] border-r border-outline-subtle': featured, 'w-full aspect-[3/4] border-b border-outline-subtle': !featured}"
    >
      <img 
        :src="getBookCover(book.title)" 
        :alt="book.title"
        class="w-full h-full object-cover"
      />
      <div v-if="featured" class="absolute top-4 right-4 flex gap-2">
        <span class="badge-dark shadow-lg backdrop-blur-md bg-primary-soft/80 border border-white/10">AI 核心推荐</span>
      </div>
      <div v-if="!featured" class="absolute top-3 left-3 flex flex-col gap-2">
        <div class="bg-white/90 backdrop-blur-md badge shadow-sm text-on-surface flex items-center justify-between gap-1 border border-outline-subtle px-2 py-1 rounded-md text-[10px] font-bold">
          <span class="material-symbols-outlined text-[12px] text-accent">star</span>
          {{ book.rating || '8.9' }}
        </div>
        <div v-if="book.emotion" class="bg-gradient-to-r from-orange-400 to-rose-400 text-white shadow-sm px-2 py-1 rounded-md text-[9px] font-extrabold uppercase tracking-widest text-center">
          {{ book.emotion }}
        </div>
      </div>
    </div>
    
    <div 
      class="flex flex-col gap-4"
      :class="{'w-full md:w-3/5 p-6 md:p-10 lg:p-12 justify-center': featured, 'p-6 flex-grow': !featured}"
    >
      <div v-if="featured" class="flex gap-2 flex-wrap mb-2">
        <span class="badge-light flex items-center gap-1 border border-outline-subtle"><span class="material-symbols-outlined text-[12px] text-accent">star</span> {{ book.rating || '9.4' }}</span>
        <span class="badge-light border border-outline-subtle">索书号: {{ book.call_number || 'I247.5' }}</span>
      </div>
      <div v-else class="flex justify-between items-start text-on-surface-muted transition-all duration-300">
         <div class="flex flex-col gap-1">
            <span class="text-xs font-bold uppercase tracking-widest text-accent">{{ book.author || '未知作者' }}</span>
            <div class="flex flex-wrap gap-1 mt-1">
               <span v-for="tag in book.tags?.slice(0, 2)" :key="tag" class="text-[9px] bg-surface-low border border-outline-subtle px-1.5 py-0.5 rounded text-on-surface-muted font-bold opacity-80"># {{ tag }}</span>
            </div>
         </div>
         <span class="material-symbols-outlined text-lg opacity-30 hover:opacity-100 hover:text-accent cursor-pointer transition-opacity" style="font-variation-settings: 'FILL' 0;">bookmark_add</span>
      </div>

      <h3 class="font-extrabold font-headline leading-tight text-on-surface" :class="{'text-3xl md:text-5xl mt-[-8px]': featured, 'text-2xl mt-[-4px]': !featured}">
        {{ book.title }}
      </h3>
      
      <p 
        class="text-accent-teal font-medium flex items-start gap-2 max-w-md"
        :class="{'italic text-lg md:text-xl': featured, 'text-sm mb-1': !featured}"
      >
        <span class="material-symbols-outlined shrink-0 mt-1" style="font-variation-settings: 'FILL' 1;" :class="{'text-sm': featured, 'text-[12px] mt-0.5': !featured}">colors_spark</span>
        <span>
           {{ showRecommendation && book.description ? 
              (featured ? book.description : book.description.substring(0, 36) + '...') 
              : ((book.author || '') + ' - ' + (book.call_number || '')) }}
        </span>
      </p>
      
      <p v-if="featured" class="text-on-surface-muted leading-relaxed max-w-lg mt-2 font-medium line-clamp-3">
        这本著作高度契合了您在搜索中表达的深层意图。系统认为它能在概念层面上为您提供极大的参考价值。
      </p>

      <div class="mt-auto flex flex-col gap-4">
        <div v-if="book.similar_books?.length > 0" class="flex flex-col gap-2 pt-4 border-t border-outline-subtle/50">
          <p class="text-[10px] font-extrabold text-on-surface-muted uppercase tracking-widest flex items-center gap-1">
            <span class="material-symbols-outlined text-[12px] text-accent-teal">auto_stories</span> 相似推荐
          </p>
          <div class="flex gap-2 pb-1 overflow-x-auto no-scrollbar">
            <div v-for="sim in book.similar_books" :key="sim.title" class="flex items-center gap-2 bg-surface-card border border-outline-subtle p-1.5 rounded-lg shrink-0 hover:border-accent/30 transition-colors cursor-pointer group/sim">
               <div class="w-6 h-8 bg-surface-low rounded overflow-hidden">
                 <img :src="getBookCover(sim.title)" class="w-full h-full object-cover group-hover/sim:scale-110 transition-transform" />
               </div>
               <div class="flex flex-col">
                 <span class="text-[10px] font-bold text-on-surface leading-none mb-0.5">{{ sim.title }}</span>
                 <span class="text-[8px] text-accent font-extrabold">{{ sim.rating }} · {{ sim.emotion }}</span>
               </div>
            </div>
          </div>
        </div>

        <div class="flex gap-3 pt-2 flex-wrap" :class="{'md:pt-4': featured}">
          <span :class="['px-3 py-1.5 text-[11px] font-extrabold rounded-full uppercase tracking-widest flex items-center shadow-sm', book.status === '在馆' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200', featured ? 'mr-auto' : '']">
            <span class="w-1.5 h-1.5 rounded-full mr-2" :class="book.status === '在馆' ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]' : 'bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.8)]'"></span>
            {{ book.status || '状态未知' }}
          </span>
          
          <div class="flex gap-2 w-full" :class="{'md:w-auto': featured}">
             <button v-if="featured" class="btn-primary py-3 px-8 text-sm flex gap-2 items-center flex-1 md:flex-none justify-center shadow-lg shadow-primary/20">
                阅读分析 <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
             </button>
             <button @click="addToLibrary" v-if="featured" class="btn-outline py-3 px-6 text-sm flex-1 md:flex-none justify-center">
                加入书库
             </button>
             <button v-if="!featured" @click="addToLibrary" class="btn-primary bg-accent-teal py-2 px-3 text-xs flex items-center gap-1 ml-auto mt-2 rounded-lg hover:bg-accent-teal/80 transition-colors">
               <span class="material-symbols-outlined text-sm">add</span> 加入书库
             </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { supabase } from '../supabase.js'

const props = defineProps({
  book: {
    type: Object,
    required: true
  },
  showRecommendation: {
    type: Boolean,
    default: true
  },
  featured: {
    type: Boolean,
    default: false
  },
  currentUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['addedToLibrary', 'showToast'])

const addToLibrary = async () => {
  if (!props.currentUser) {
    emit('showToast', { message: '请先登录后再加入书库', type: 'warning' })
    return
  }
  
  if (props.book.status === '借出') {
    emit('showToast', { message: `《${props.book.title}》当前已被借出，暂时无法加入书库！`, type: 'warning' })
    return
  }
  
  const userId = parseInt(props.currentUser.id) || 0
  if (userId > 2147483647 || userId < 1) {
    emit('showToast', { message: '用户ID无效，请重新登录', type: 'error' })
    return
  }
  
  const title = props.book.title || ''
  
  const { data: existingUsers, error: userCheckError } = await supabase
    .from('users')
    .select('id')
    .eq('id', userId)
    .limit(1)
  
  if (userCheckError) {
    console.error('检查用户失败:', userCheckError)
  }
  
  if (!existingUsers || existingUsers.length === 0) {
    const { error: insertUserError } = await supabase
      .from('users')
      .insert([{
        id: userId,
        username: props.currentUser.username || '匿名用户',
        email: props.currentUser.email || '',
        password: 'encrypted'
      }])
    
    if (insertUserError) {
      console.error('创建用户失败:', insertUserError)
      emit('showToast', { message: `创建用户失败：${insertUserError.message}`, type: 'error' })
      return
    }
  }
  
  const { data: existingBooks, error: checkError } = await supabase
    .from('library_books')
    .select('*')
    .eq('title', title)
    .eq('user_id', String(userId))
    .limit(1)
  
  if (checkError) {
    console.error('检查书库失败:', checkError)
    emit('showToast', { message: `检查书库失败：${checkError.message}`, type: 'error' })
    return
  }
  
  if (existingBooks && existingBooks.length > 0) {
    emit('showToast', { message: `《${props.book.title}》已在书库中，无需重复添加！`, type: 'info' })
    return
  }
  
  const { error } = await supabase
    .from('library_books')
    .insert([{
      user_id: String(userId),
      title: props.book.title,
      author: props.book.author || '未知作者',
      call_number: props.book.call_number || '',
      status: '在馆',
      cover_url: getBookCover(props.book.title)
    }])
  
  if (error) {
    console.error('加入书库失败:', error)
    emit('showToast', { message: `加入书库失败：${error.message}`, type: 'error' })
    return
  }
  
  emit('addedToLibrary', props.book)
}

const getBookCover = (title) => {
  if (!title) return 'https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800&q=80'
  
  if (title.includes('三体')) return 'https://lh3.googleusercontent.com/aida-public/AB6AXuAhhKEcvhIKMw4rHgOiyb0jWxuvGz77_P5Zmtk2Q86RzUBNKNxjtiwh1KF3Q0MSwk2VCHfn5A6uQMwcW4bvAA6M-E-rwY0IkGHVz2H-FqtmbMiYo3A_MMywWUSnMUVriLLVWAj1LRbsaPpUOP-Aemmc_BD-vQ71vS_fzGgDYLzYvw2owfr0ogONAuLNaHLgljWi9ecc7JoLVVLV4RtIiEVnZxPBpiWTp13tx8mqs8EfHGa3Us_6bCxzvAMAJN0333vkXNQ12JV8pes'
  if (title.includes('基地')) return 'https://lh3.googleusercontent.com/aida-public/AB6AXuAvkknSicCX7BirXctdSa13xDUajM-3j-JzJ154X4jNA-_s7iFTCd9E73kix7sLxT12Fb93DYy9AwzEgQsCqO1pB7G7Vl1G7-jVMUnnsAxzmfxZVhoPL-z1G6T3_fLv4eqxEhEb2MpHvDTmOz33vEhiYhN0Z2c2JYxmqyu5V4pr4MFNw3chNxSZWTblf129NahdFJMK4HX-tttIleaS-cJnYVV4aNu1oYbIGSTdrar5K9QPrXbP0z5jOSvjkzXcj83Bcj4l95W0KvE'
  if (title.includes('森林')) return 'https://lh3.googleusercontent.com/aida-public/AB6AXuAVHwMVif-kpG2Fnm6A_bu-FYJSkLvdifqEH-rnK6yERC3kPBcOv59FfBfzqU85KSA2Uh30hQsKhJ3zpybuaLLPkUKs0txXRiCNJTHVIGzpEXHowNleiK_odjlBWLBNr5kcPxOoBdJnvvinu1hMJ11-PMOW6nEyrFKWE0bGPpSDnoPFRSwEDWcfZ5us14p2xNhKIEs3G4mWvup58pakiFc09ZKRonmx18jPKb07yHRnvMgsWhBXwmPIFfZwAuB8kfsy1IVM7frXFxg'
  
  const covers = [
    'https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800&q=80',
    'https://images.unsplash.com/photo-1550399105-c4eb705e46ce?w=800&q=80',
    'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
    'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&q=80'
  ]
  
  let hash = 0
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % covers.length
  return covers[index]
}
</script>

<style scoped>
</style>