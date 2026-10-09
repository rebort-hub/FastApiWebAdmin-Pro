<template>
  <div v-if="showWorkTab" class="ntesterc-work-tab">
    <div ref="scrollRef" class="ntesterc-work-tab__scroll">
      <div class="ntesterc-work-tab__list">
        <a-dropdown
          v-for="tab in tabs"
          :key="tab.path"
          :trigger="['contextmenu']"
        >
          <div
            class="ntesterc-work-tab__item"
            :class="{ 'ntesterc-work-tab__item--active': tab.path === activePath }"
            @click="goTab(tab.path)"
          >
            <span class="ntesterc-work-tab__label">{{ tab.title }}</span>
            <CloseOutlined
              v-if="!tab.fixedTab && tabs.length > 1"
              class="ntesterc-work-tab__close"
              @click.stop="closeTab(tab.path)"
            />
          </div>
          <template #overlay>
            <NtestercWorkTabMenu :tab-path="tab.path" @action="onMenuAction" />
          </template>
        </a-dropdown>
      </div>
    </div>
    <a-dropdown :trigger="['click']">
      <a-button type="text" class="ntesterc-work-tab__more">
        <DownOutlined />
      </a-button>
      <template #overlay>
        <NtestercWorkTabMenu :tab-path="route.path" @action="onMenuAction" />
      </template>
    </a-dropdown>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { CloseOutlined, DownOutlined } from '@ant-design/icons-vue'
import type { RootState } from '@/types/store'
import { useNtestercSettings } from '@/composables/useNtestercSettings'
import NtestercWorkTabMenu from './NtestercWorkTabMenu.vue'

defineOptions({ name: 'NtestercWorkTab' })

const store = useStore<RootState>()
const router = useRouter()
const route = useRoute()
const { settings } = useNtestercSettings()

const scrollRef = ref<HTMLElement | null>(null)

const showWorkTab = computed(() => settings.value.showWorkTab)
const tabs = computed(() => store.state.worktab.opened)
const activePath = computed(() => route.path)

function goTab(path: string) {
  if (path === route.path) return
  router.push(path)
}

function closeTab(path: string) {
  const tab = store.state.worktab.opened.find((t) => t.path === path)
  if (!tab || tab.fixedTab) return
  store.commit('worktab/removeTab', path)
  if (route.path === path) {
    const fallback =
      store.state.worktab.opened[store.state.worktab.opened.length - 1]?.path ?? '/dashboard/workplace'
    router.push(fallback)
  }
}

function onMenuAction(action: string, path: string) {
  switch (action) {
    case 'refresh':
      if (route.path === path) {
        router.replace({ path: route.path, query: { ...route.query, _r: String(Date.now()) } })
      } else {
        router.push(path)
      }
      break
    case 'close':
      closeTab(path)
      break
    case 'closeOther':
      store.commit('worktab/removeOtherTabs', path)
      if (!store.state.worktab.opened.some((t) => t.path === route.path)) {
        router.push(path)
      }
      break
    case 'closeLeft':
      store.commit('worktab/removeLeftTabs', path)
      if (!store.state.worktab.opened.some((t) => t.path === route.path)) {
        router.push(path)
      }
      break
    case 'closeRight':
      store.commit('worktab/removeRightTabs', path)
      if (!store.state.worktab.opened.some((t) => t.path === route.path)) {
        router.push(path)
      }
      break
    case 'closeAll':
      store.commit('worktab/removeAllTabs')
      router.push(store.state.worktab.activePath)
      break
  }
}
</script>

<style lang="scss" scoped>
.ntesterc-work-tab {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 40px;
  padding: 0 12px 0 8px;
  background: var(--ntesterc-header-bg);
  border-bottom: 1px solid var(--ntesterc-border);

  &__scroll {
    flex: 1;
    min-width: 0;
    overflow-x: auto;
    overflow-y: hidden;

    &::-webkit-scrollbar {
      height: 4px;
    }
  }

  &__list {
    display: flex;
    gap: 6px;
    align-items: center;
    min-width: min-content;
    padding: 4px 0;
  }

  &__item {
    display: inline-flex;
    gap: 6px;
    align-items: center;
    max-width: 160px;
    padding: 4px 10px;
    font-size: 13px;
    color: var(--ntesterc-text-secondary);
    cursor: pointer;
    background: var(--ntesterc-card-bg);
    border: 1px solid var(--ntesterc-border);
    border-radius: 6px;
    transition: all 0.15s ease;

    &:hover {
      color: var(--ntesterc-text);
      border-color: var(--ntesterc-primary, #1677ff);
    }

    &--active {
      color: var(--ntesterc-primary, #1677ff);
      background: var(--ntesterc-menu-active);
      border-color: var(--ntesterc-border);
    }
  }

  &__label {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__close {
    flex-shrink: 0;
    font-size: 10px;
    opacity: 0.65;

    &:hover {
      opacity: 1;
    }
  }

  &__more {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    padding: 0;
    border-radius: 6px;
  }
}
</style>
