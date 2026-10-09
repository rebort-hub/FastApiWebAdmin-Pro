<template>
  <div class="ntesterc-admin-layout" :class="`ntesterc-admin-layout--${menuLayout}`">
    <div class="ntesterc-admin-layout__shell">
      <div v-if="showDualRail" class="ntesterc-dual-rail">
        <div class="ntesterc-dual-rail__brand" @click="goHome">
          <NtestercLogo :collapsed="true" :title="appTitle" />
        </div>
        <div class="ntesterc-dual-rail__list">
          <button
            v-for="item in topLevelMenus"
            :key="item.key"
            type="button"
            class="ntesterc-dual-rail__item"
            :class="{ 'is-active': item.key === activeRootKey }"
            :title="item.title"
            @click="onRootMenuClick(item)"
          >
            <component :is="item.iconComp" v-if="item.iconComp" />
            <span v-else>{{ item.title.slice(0, 1) }}</span>
          </button>
        </div>
      </div>

      <NtestercSidebar
        v-if="showSidebar"
        :app-title="appTitle"
        :collapsed="sidebarCollapsed"
        :hide-brand="menuLayout === 'dual'"
        :items="sideMenuItems"
        v-model:selected-keys="menuState.selectedKeys"
        v-model:open-keys="menuState.openKeys"
        @home="goHome"
        @menu-click="handleMenuClick"
      />

      <div class="ntesterc-admin-layout__main">
        <NtestercHeaderBar
          :collapsed="collapsed"
          :breadcrumb-items="headerBreadcrumbs"
          :username="String(store.state.user.basicInfo.username ?? '')"
          :avatar="String(store.state.user.basicInfo.avatar ?? '')"
          :avatar-fallback="avatarFallback"
          :app-title="appTitle"
          :show-collapse="showCollapse"
          :show-logo="menuLayout === 'horizontal'"
          :hide-breadcrumb="menuLayout === 'horizontal'"
          @toggle-collapse="collapsed = !collapsed"
          @open-settings="settingsOpen = true"
          @user-menu="onUserMenu"
          @home="goHome"
        >
          <template v-if="showHeaderMenu" #nav>
            <a-menu
              mode="horizontal"
              :selected-keys="headerSelectedKeys"
              :items="headerMenuItems"
              @click="onHeaderMenuClick"
            />
          </template>
        </NtestercHeaderBar>
        <NtestercWorkTab />
        <NtestercPageContent />
      </div>
    </div>
    <NtestercSettingsPanel v-model="settingsOpen" />
  </div>
</template>

<script lang="ts" setup>
import { computed, h, onMounted, reactive, ref, watch, type Component } from 'vue'
import type { MenuProps } from 'ant-design-vue'
import type { ItemType } from 'ant-design-vue/es/menu/src/interface'
import { useRoute, useRouter } from 'vue-router'
import storage from 'store'
import * as icons from '@ant-design/icons-vue'
import store from '@/store'
import { listToTree } from '@/utils/util'
import { useNtestercSettings } from '@/composables/useNtestercSettings'
import NtestercSidebar from '@/components/ntesterc/NtestercSidebar.vue'
import NtestercHeaderBar from '@/components/ntesterc/NtestercHeaderBar.vue'
import NtestercPageContent from '@/components/ntesterc/NtestercPageContent.vue'
import NtestercWorkTab from '@/components/ntesterc/NtestercWorkTab.vue'
import NtestercSettingsPanel from '@/components/ntesterc/NtestercSettingsPanel.vue'
import NtestercLogo from '@/components/ntesterc/NtestercLogo.vue'
import type { NtestercBreadcrumbItem } from '@/components/ntesterc/NtestercBreadcrumb.vue'
import type { NtestercMenuLayout } from '@/types/app'

defineOptions({ name: 'NtestercAdminLayout' })

interface LayoutMenuItem {
  key: string
  label: string
  title: string
  icon?: () => ReturnType<typeof h>
  iconComp?: Component
  children?: LayoutMenuItem[]
}

const appTitle = 'FastApiWebAdmin'

const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const settingsOpen = ref(false)
const { settings } = useNtestercSettings()

const menuState = reactive({
  openKeys: [] as string[],
  selectedKeys: [route.path] as string[],
  menus: [] as LayoutMenuItem[],
})

const activeRootKey = ref('')
const menuLayout = computed<NtestercMenuLayout>(() => settings.value.menuLayout)
const showCollapse = computed(() => menuLayout.value === 'vertical' || menuLayout.value === 'mixed')
const showDualRail = computed(() => menuLayout.value === 'dual')
const showHeaderMenu = computed(
  () => menuLayout.value === 'horizontal' || menuLayout.value === 'mixed',
)
const sidebarCollapsed = computed(() =>
  menuLayout.value === 'vertical' || menuLayout.value === 'mixed' ? collapsed.value : false,
)

const avatarFallback = computed(() => {
  const name = store.state.user.basicInfo.username
  return name ? String(name).charAt(0).toUpperCase() : 'U'
})

const headerBreadcrumbs = computed<NtestercBreadcrumbItem[]>(() => {
  const items: NtestercBreadcrumbItem[] = []
  route.matched.forEach((item, index) => {
    if (index !== 0 && item.meta?.title) {
      items.push({ path: item.path, title: String(item.meta.title) })
    }
  })
  return items
})

const topLevelMenus = computed(() => menuState.menus)

const headerMenuItems = computed<ItemType[]>(() => {
  if (menuLayout.value === 'horizontal') return menuState.menus as ItemType[]
  return topLevelMenus.value.map((item) => ({
    key: item.key,
    label: item.label,
    title: item.title,
    icon: item.icon,
  }))
})

const headerSelectedKeys = computed(() => {
  if (menuLayout.value === 'mixed' || menuLayout.value === 'dual') {
    return activeRootKey.value ? [activeRootKey.value] : []
  }
  return menuState.selectedKeys
})

const activeRootMenu = computed(
  () => topLevelMenus.value.find((item) => item.key === activeRootKey.value) ?? null,
)

const sideMenuItems = computed<ItemType[]>(() => {
  if (menuLayout.value === 'vertical') return menuState.menus as ItemType[]
  return (activeRootMenu.value?.children ?? []) as ItemType[]
})

const showSidebar = computed(() => {
  if (menuLayout.value === 'horizontal') return false
  if (menuLayout.value === 'vertical') return true
  return sideMenuItems.value.length > 0
})

function firstLeafKey(item: LayoutMenuItem): string {
  if (item.children?.length) return firstLeafKey(item.children[0])
  return item.key
}

function findRootKey(items: LayoutMenuItem[], path: string): string {
  for (const item of items) {
    if (item.key === path) return item.key
    if (item.children?.length && containsPath(item.children, path)) return item.key
  }
  return items[0]?.key ?? ''
}

function containsPath(items: LayoutMenuItem[], path: string): boolean {
  return items.some((item) => item.key === path || (item.children && containsPath(item.children, path)))
}

function syncActiveRoot(path: string) {
  activeRootKey.value = findRootKey(menuState.menus, path)
}

function goHome() {
  router.push('/dashboard/workplace')
}

function onRootMenuClick(item: LayoutMenuItem) {
  activeRootKey.value = item.key
  router.push(firstLeafKey(item))
}

const handleMenuClick: MenuProps['onClick'] = (menuInfo) => {
  if (menuInfo.keyPath?.length) {
    menuState.openKeys = [String(menuInfo.keyPath[0])]
  }
  router.push(String(menuInfo.key))
}

const onHeaderMenuClick: MenuProps['onClick'] = (menuInfo) => {
  const key = String(menuInfo.key)
  if (menuLayout.value === 'mixed') {
    const item = topLevelMenus.value.find((m) => m.key === key)
    if (item) {
      onRootMenuClick(item)
      return
    }
  }
  router.push(key)
}

function onUserMenu(key: string) {
  if (key === 'profile') {
    router.push('/profile')
    return
  }
  storage.remove('Access-Token')
  storage.remove('Refresh-Token')
  store.dispatch('clearUserInfo').then(() => {
    router.push('/login')
  })
}

watch(
  () => route.path,
  (newPath) => {
    menuState.selectedKeys = [newPath]
    syncActiveRoot(newPath)
    const routePaths = store.state.user.routeList.map((item) => item.route_path)
    if (!routePaths.includes(newPath)) {
      menuState.openKeys = []
      menuState.selectedKeys = []
    }
  },
)

watch(
  () => menuState.menus,
  () => syncActiveRoot(route.path),
)

interface MenuRouteRow {
  route_path: string
  name: string
  icon?: string
  hidden?: boolean
  children?: MenuRouteRow[]
}

let currentParentPath = ''
let findCurrentParentPathStop = false

function menuGenerator(routers: MenuRouteRow[]): LayoutMenuItem[] {
  const routerList: LayoutMenuItem[] = []
  for (const item of routers) {
    if (item.hidden) continue

    let icon: (() => ReturnType<typeof h>) | undefined
    let iconComp: Component | undefined
    if (item.icon && item.icon in icons) {
      const IconComp = icons[item.icon as keyof typeof icons] as Component
      iconComp = IconComp
      icon = () => h(IconComp)
    }

    if (item.route_path === route.path) {
      findCurrentParentPathStop = true
      menuState.openKeys = [currentParentPath]
    }

    const routerItem: LayoutMenuItem = {
      key: item.route_path,
      label: item.name,
      title: item.name,
      icon,
      iconComp,
    }

    if (item.children?.length) {
      if (!findCurrentParentPathStop) {
        currentParentPath = item.route_path
      }
      routerItem.children = menuGenerator(item.children)
    }

    routerList.push(routerItem)
  }
  return routerList
}

onMounted(() => {
  const menuTree = listToTree(store.state.user.routeList)
  menuState.menus = menuGenerator(menuTree as MenuRouteRow[])
  syncActiveRoot(route.path)
})
</script>

<style lang="scss" scoped>
.ntesterc-admin-layout {
  height: 100%;
  overflow: hidden;

  &__shell {
    display: flex;
    height: 100%;
    overflow: hidden;
  }

  &__main {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-width: 0;
    min-height: 0;
    overflow: hidden;
    background: var(--ntesterc-bg);
  }
}

.ntesterc-dual-rail {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  width: 64px;
  background: var(--ntesterc-sider-bg);
  border-right: 1px solid var(--ntesterc-border);

  &__brand {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 56px;
    border-bottom: 1px solid var(--ntesterc-border);
    cursor: pointer;
  }

  &__list {
    display: flex;
    flex: 1;
    flex-direction: column;
    gap: 4px;
    padding: 8px 6px;
    overflow: auto;
  }

  &__item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 44px;
    font-size: 16px;
    color: var(--ntesterc-text-secondary);
    cursor: pointer;
    background: transparent;
    border: none;
    border-radius: 8px;

    &:hover,
    &.is-active {
      color: var(--ntesterc-primary);
      background: var(--ntesterc-menu-active);
    }
  }
}
</style>
