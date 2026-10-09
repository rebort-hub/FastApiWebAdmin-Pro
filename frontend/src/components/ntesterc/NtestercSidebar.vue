<template>
  <aside
    class="ntesterc-sidebar"
    :class="{
      'ntesterc-sidebar--collapsed': collapsed,
      'ntesterc-sidebar--no-brand': hideBrand,
    }"
  >
    <div v-if="!hideBrand" class="ntesterc-sidebar__brand">
      <NtestercLogo :collapsed="collapsed" :title="appTitle" @click="emit('home')" />
    </div>
    <div class="ntesterc-sidebar__menu">
      <a-menu
        v-model:selectedKeys="selectedKeysModel"
        v-model:openKeys="openKeysModel"
        mode="inline"
        :inline-collapsed="collapsed"
        :items="items"
        @click="onMenuClick"
      />
    </div>
  </aside>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { MenuProps } from 'ant-design-vue'
import type { ItemType } from 'ant-design-vue/es/menu/interface'
import NtestercLogo from './NtestercLogo.vue'

defineOptions({ name: 'NtestercSidebar' })

const props = withDefaults(
  defineProps<{
    appTitle?: string
    collapsed?: boolean
    hideBrand?: boolean
    items?: ItemType[]
    selectedKeys?: string[]
    openKeys?: string[]
  }>(),
  {
    appTitle: 'FastApiWebAdmin',
    collapsed: false,
    hideBrand: false,
    items: () => [],
    selectedKeys: () => [],
    openKeys: () => [],
  },
)

const emit = defineEmits<{
  home: []
  menuClick: [info: Parameters<NonNullable<MenuProps['onClick']>>[0]]
  'update:selectedKeys': [keys: string[]]
  'update:openKeys': [keys: string[]]
}>()

const selectedKeysModel = computed({
  get: () => props.selectedKeys,
  set: (v) => emit('update:selectedKeys', v as string[]),
})

const openKeysModel = computed({
  get: () => props.openKeys,
  set: (v) => emit('update:openKeys', v as string[]),
})

function onMenuClick(info: Parameters<NonNullable<MenuProps['onClick']>>[0]) {
  emit('menuClick', info)
}
</script>

<style lang="scss" scoped>
.ntesterc-sidebar {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  width: 220px;
  height: 100%;
  max-height: 100%;
  overflow: hidden;
  background: var(--ntesterc-sider-bg);
  border-right: 1px solid var(--ntesterc-border);
  transition: width 0.2s ease;

  /* 与 ant-menu-inline-collapsed 默认宽度（约 80px）一致，避免横向溢出滚动条 */
  &--collapsed {
    width: 80px;
  }

  &__brand {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    height: 56px;
    padding: 0 16px;
    border-bottom: 1px solid var(--ntesterc-border);
  }

  &--collapsed &__brand {
    justify-content: center;
    padding: 0;
    overflow: hidden;
  }

  &__menu {
    flex: 1;
    min-height: 0;
    min-width: 0;
    padding: 8px 0;
    overflow-x: hidden;
    overflow-y: auto;

    :deep(.ant-menu) {
      background: transparent;
      border-inline-end: none !important;
    }

    :deep(.ant-menu-item),
    :deep(.ant-menu-submenu-title) {
      margin-inline: 8px;
      width: calc(100% - 16px);
      border-radius: 8px;
    }

    :deep(.ant-menu-item-selected) {
      background: var(--ntesterc-menu-active) !important;
    }

    :deep(.ant-menu-item:not(.ant-menu-item-selected):hover),
    :deep(.ant-menu-submenu-title:hover) {
      background: var(--ntesterc-menu-hover);
    }
  }

  &--collapsed &__menu {
    padding: 8px 0;
    overflow-x: hidden;

    :deep(.ant-menu.ant-menu-inline-collapsed) {
      width: 100% !important;
    }

    :deep(.ant-menu-item),
    :deep(.ant-menu-submenu-title) {
      margin-inline: 0;
      width: 100%;
      border-radius: 0;
    }
  }
}
</style>
