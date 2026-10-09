import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import type { RootState } from '@/types/store'
import type { WorkTabItem } from '@/types/worktab'

const SKIP_PATHS = new Set(['/login', '/forget-password', '/404'])

export function useNtestercWorkTabRouteSync() {
  const route = useRoute()
  const store = useStore<RootState>()

  watch(
    () => route.fullPath,
    () => {
      if (SKIP_PATHS.has(route.path) || route.name === '404') return
      const title = route.meta?.title ? String(route.meta.title) : String(route.name ?? route.path)
      const tab: WorkTabItem = {
        path: route.path,
        title,
        name: route.name ? String(route.name) : undefined,
        keepAlive: Boolean(route.meta?.keepAlive),
        fixedTab: route.path === '/dashboard/workplace',
      }
      store.commit('worktab/openTab', tab)
    },
    { immediate: true },
  )
}
