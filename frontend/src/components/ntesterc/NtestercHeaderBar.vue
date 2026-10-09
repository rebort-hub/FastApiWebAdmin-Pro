<template>
  <header class="ntesterc-header-bar">
    <div class="ntesterc-header-bar__left">
      <a-button
        v-if="showCollapse"
        type="text"
        class="ntesterc-header-bar__trigger"
        @click="emit('toggleCollapse')"
      >
        <MenuUnfoldOutlined v-if="collapsed" />
        <MenuFoldOutlined v-else />
      </a-button>
      <NtestercLogo
        v-if="showLogo"
        class="ntesterc-header-bar__logo"
        :collapsed="false"
        :title="appTitle"
        @click="emit('home')"
      />
      <div v-if="$slots.nav" class="ntesterc-header-bar__nav">
        <slot name="nav" />
      </div>
      <NtestercBreadcrumb
        v-if="showBreadcrumb && breadcrumbItems.length && !hideBreadcrumb"
        :items="breadcrumbItems"
      />
    </div>
    <div class="ntesterc-header-bar__right">
      <a-tooltip title="主题设置">
        <a-button type="text" class="ntesterc-header-bar__icon-btn" @click="emit('openSettings')">
          <SettingOutlined />
        </a-button>
      </a-tooltip>
      <a-tooltip :title="isDark ? '切换浅色' : '切换深色'">
        <a-button type="text" class="ntesterc-header-bar__icon-btn" @click="toggleTheme">
          <BulbOutlined v-if="isDark" />
          <BulbFilled v-else />
        </a-button>
      </a-tooltip>
      <a-dropdown>
        <div class="ntesterc-header-bar__user" @click.prevent>
          <a-avatar :src="avatar" :size="32">{{ avatarFallback }}</a-avatar>
          <span class="ntesterc-header-bar__username">{{ username }}</span>
        </div>
        <template #overlay>
          <a-menu @click="onUserMenu">
            <a-menu-item key="profile">个人中心</a-menu-item>
            <a-menu-item key="logout">退出登录</a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </header>
</template>

<script lang="ts" setup>
import {
  BulbFilled,
  BulbOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  SettingOutlined,
} from '@ant-design/icons-vue'
import type { MenuProps } from 'ant-design-vue'
import { computed } from 'vue'
import NtestercBreadcrumb, { type NtestercBreadcrumbItem } from './NtestercBreadcrumb.vue'
import NtestercLogo from './NtestercLogo.vue'
import { useNtestercSettings } from '@/composables/useNtestercSettings'
import { useNtestercTheme } from '@/composables/useNtestercTheme'

defineOptions({ name: 'NtestercHeaderBar' })

const props = withDefaults(
  defineProps<{
    collapsed?: boolean
    breadcrumbItems?: NtestercBreadcrumbItem[]
    username?: string
    avatar?: string
    avatarFallback?: string
    appTitle?: string
    showCollapse?: boolean
    showLogo?: boolean
    hideBreadcrumb?: boolean
  }>(),
  {
    collapsed: false,
    breadcrumbItems: () => [],
    appTitle: 'FastApiWebAdmin',
    showCollapse: true,
    showLogo: false,
    hideBreadcrumb: false,
  },
)

const emit = defineEmits<{
  toggleCollapse: []
  openSettings: []
  userMenu: [key: string]
  home: []
}>()

const { settings, patchSettings } = useNtestercSettings()
const { isDark } = useNtestercTheme()
const showBreadcrumb = computed(() => settings.value.showBreadcrumb && !props.hideBreadcrumb)

function toggleTheme() {
  patchSettings({ themeMode: isDark.value ? 'light' : 'dark' })
}

const onUserMenu: MenuProps['onClick'] = ({ key }) => {
  emit('userMenu', String(key))
}
</script>

<style lang="scss" scoped>
.ntesterc-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 16px 0 8px;
  background: var(--ntesterc-header-bg);
  border-bottom: 1px solid var(--ntesterc-border);
  backdrop-filter: blur(8px);

  &__left,
  &__right {
    display: flex;
    gap: 8px;
    align-items: center;
    min-width: 0;
  }

  &__left {
    flex: 1;
  }

  &__nav {
    flex: 1;
    min-width: 0;
    overflow: hidden;

    :deep(.ant-menu-horizontal) {
      line-height: 54px;
      background: transparent;
      border-bottom: none;
    }
  }

  &__logo {
    width: auto;
    margin-right: 8px;
  }

  &__trigger,
  &__icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    font-size: 16px;
    color: var(--ntesterc-text-secondary);
    border-radius: 8px;

    &:hover {
      color: var(--ntesterc-text);
      background: var(--ntesterc-menu-hover);
    }
  }

  &__user {
    display: flex;
    gap: 8px;
    align-items: center;
    padding: 4px 8px;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.2s;

    &:hover {
      background: var(--ntesterc-menu-hover);
    }
  }

  &__username {
    max-width: 120px;
    overflow: hidden;
    font-size: 14px;
    color: var(--ntesterc-text);
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
