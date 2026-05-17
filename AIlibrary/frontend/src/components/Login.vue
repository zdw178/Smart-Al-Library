<template>
  <div class="min-h-screen bg-gradient-to-br from-[#0D9488] via-[#6366F1] to-[#8B5CF6] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden">
      <div class="p-8">
        <div class="text-center mb-8">
          <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-[#0D9488] to-[#6366F1] flex items-center justify-center">
            <span class="material-symbols-outlined text-white text-3xl" style="font-variation-settings: 'FILL' 1;">menu_book</span>
          </div>
          <h1 class="text-3xl font-black tracking-tight mb-2">SmartLib AI</h1>
          <p class="text-gray-500">智能图书馆系统</p>
        </div>

        <div class="flex mb-6 bg-gray-100 rounded-xl p-1">
          <button 
            @click="isLogin = true" 
            class="flex-1 py-2.5 rounded-lg text-sm font-bold transition-all"
            :class="isLogin ? 'bg-white shadow-sm text-black' : 'text-gray-500'"
          >
            登录
          </button>
          <button 
            @click="isLogin = false" 
            class="flex-1 py-2.5 rounded-lg text-sm font-bold transition-all"
            :class="!isLogin ? 'bg-white shadow-sm text-black' : 'text-gray-500'"
          >
            注册
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div v-if="!isLogin">
            <label class="block text-sm font-bold text-gray-700 mb-2">用户名</label>
            <input 
              v-model="username" 
              type="text" 
              required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-[#0D9488]/20 focus:border-[#0D9488] outline-none transition-all"
              placeholder="请输入用户名"
            />
          </div>

          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">邮箱</label>
            <input 
              v-model="email" 
              type="email" 
              required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-[#0D9488]/20 focus:border-[#0D9488] outline-none transition-all"
              placeholder="请输入邮箱"
            />
          </div>

          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">密码</label>
            <input 
              v-model="password" 
              type="password" 
              required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-[#0D9488]/20 focus:border-[#0D9488] outline-none transition-all"
              placeholder="请输入密码"
            />
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm">
            {{ error }}
          </div>

          <div v-if="success" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-xl text-sm">
            {{ success }}
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full py-3 bg-gradient-to-r from-[#0D9488] to-[#6366F1] text-white font-bold rounded-xl hover:opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="material-symbols-outlined animate-spin">progress_activity</span>
            {{ isLogin ? '登录' : '注册' }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          {{ isLogin ? '还没有账号？' : '已有账号？' }}
          <button @click="isLogin = !isLogin" class="text-[#0D9488] font-bold hover:underline">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['loginSuccess'])

const isLogin = ref(true)
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleSubmit = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      await handleLogin()
    } else {
      await handleRegister()
    }
  } finally {
    loading.value = false
  }
}

const handleLogin = async () => {
  const users = JSON.parse(localStorage.getItem('smartlib_users') || '[]')
  const user = users.find(u => u.email === email.value && u.password === password.value)
  
  if (!user) {
    error.value = '邮箱或密码错误'
    return
  }

  localStorage.setItem('currentUser', JSON.stringify(user))
  emit('loginSuccess', user)
}

const handleRegister = async () => {
  if (!username.value.trim()) {
    error.value = '请输入用户名'
    return
  }

  const users = JSON.parse(localStorage.getItem('smartlib_users') || '[]')
  
  const existingUser = users.find(u => u.email === email.value)
  if (existingUser) {
    error.value = '该邮箱已被注册'
    return
  }

  const existingUsername = users.find(u => u.username === username.value)
  if (existingUsername) {
    error.value = '该用户名已被使用'
    return
  }

  const newUser = {
    id: Math.floor(Date.now() / 1000) % 1000000000,
    username: username.value,
    email: email.value,
    password: password.value,
    created_at: new Date().toISOString()
  }

  users.push(newUser)
  localStorage.setItem('smartlib_users', JSON.stringify(users))

  success.value = '注册成功！正在登录...'
  setTimeout(() => {
    localStorage.setItem('currentUser', JSON.stringify(newUser))
    emit('loginSuccess', newUser)
  }, 1000)
}
</script>

<style scoped>
</style>