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

<style>
@import '@/styles/ntesterc-theme.scss';
@import '@/styles/ntesterc-scrollbar.scss';
@import '@/styles/ntesterc-modal.scss';

* {
  margin: 0;
  padding: 0;
}

html,
body,
#app {
  margin: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--ntesterc-bg);
}

#app {
  display: flex;
  flex-direction: column;
}

/* ConfigProvider 等中间节点需参与撑满视口 */
#app > * {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  width: 100%;
}

.ntesterc-app {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: var(--ntesterc-text);
  background: var(--ntesterc-bg);
}

/* 仅布局路由根节点撑满，避免影响固定定位的全局 Loading */
.ntesterc-app > .ntesterc-admin-layout {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.ant-page-header {
  padding: 20px 0;
}

.ant-modal .ant-modal-header {
  margin-bottom: 20px;
}

.ntesterc-settings-drawer .ant-drawer-footer {
  padding: 12px 20px 16px;
  border-top: 1px solid var(--ntesterc-border);
}
</style>
