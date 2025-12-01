import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import './assets/main.css' 

axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.withCredentials = true

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.use(router)
app.mount('#app')
