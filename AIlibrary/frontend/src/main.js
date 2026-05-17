import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { supabase } from './supabase.js'

const app = createApp(App)

app.config.globalProperties.$supabase = supabase
app.provide('supabase', supabase)

app.mount('#app')