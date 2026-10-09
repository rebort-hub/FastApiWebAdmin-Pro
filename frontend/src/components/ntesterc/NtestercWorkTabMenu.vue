<template>
  <a-menu class="ntesterc-work-tab-menu" @click="onClick">
    <a-menu-item key="refresh">刷新</a-menu-item>
    <a-menu-divider />
    <a-menu-item key="close" :disabled="!state.closable">关闭</a-menu-item>
    <a-menu-item key="closeOther" :disabled="!state.canCloseOther">关闭其他</a-menu-item>
    <a-menu-item key="closeLeft" :disabled="!state.canCloseLeft">关闭左侧</a-menu-item>
    <a-menu-item key="closeRight" :disabled="!state.canCloseRight">关闭右侧</a-menu-item>
    <a-menu-divider />
    <a-menu-item key="closeAll" :disabled="!state.canCloseAll">关闭全部</a-menu-item>
  </a-menu>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { MenuProps } from 'ant-design-vue'
import { useStore } from 'vuex'
import type { RootState } from '@/types/store'

defineOptions({ name: 'NtestercWorkTabMenu' })

const props = defineProps<{
  tabPath: string
}>()

const emit = defineEmits<{
  action: [key: string, tabPath: string]
}>()

const store = useStore<RootState>()

const state = computed(() => {
  const opened = store.state.worktab.opened
  const index = opened.findIndex((t) => t.path === props.tabPath)
  const tab = opened[index]
  const fixed = Boolean(tab?.fixedTab)

  const closable = Boolean(tab && !fixed && opened.length > 1)

  const hasClosableLeft = opened.slice(0, index).some((t) => !t.fixedTab)
  const hasClosableRight = opened.slice(index + 1).some((t) => !t.fixedTab)
  const closableCount = opened.filter((t) => !t.fixedTab).length

  return {
    closable,
    canCloseOther: closableCount > 1 && (closable || !fixed),
    canCloseLeft: hasClosableLeft,
    canCloseRight: hasClosableRight,
    canCloseAll: closableCount > 0,
  }
})

const onClick: MenuProps['onClick'] = ({ key }) => {
  emit('action', String(key), props.tabPath)
}
</script>

<style lang="scss" scoped>
.ntesterc-work-tab-menu {
  min-width: 140px;
}
</style>
