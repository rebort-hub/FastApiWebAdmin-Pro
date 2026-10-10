import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { bindAppStore } from '@/utils/appStoreBridge'
import Antd from 'ant-design-vue'
import VChart from 'vue-echarts'
import 'echarts'
import '@/styles'

const app = createApp(App)
app.use(router)
app.use(store)
bindAppStore(store)
app.use(Antd)
app.component('VChart', VChart)
app.mount('#app')
