<template>
  <ConfigProvider :locale="zhCN" :theme="antdTheme">
    <div class="ntesterc-app">
      <router-view />
      <NtestercNprogress />
      <NtestercGlobalLoading />
    </div>
  </ConfigProvider>
</template>

<script lang="ts" setup>
import { ConfigProvider } from 'ant-design-vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import { useNtestercTheme } from '@/composables/useNtestercTheme'
import NtestercGlobalLoading from '@/components/ntesterc/NtestercGlobalLoading.vue'
import NtestercNprogress from '@/components/ntesterc/NtestercNprogress.vue'

dayjs.locale('zh-cn')

const { antdTheme } = useNtestercTheme()

window.addEventListener('unhandledrejection', function browserRejectionHandler(event) {
  event && event.preventDefault()
})
</script>

