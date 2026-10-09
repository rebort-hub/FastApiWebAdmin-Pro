import type { Store } from 'vuex'
import type { RootState } from '@/types/store'
import type { NtestercAppSettings } from '@/types/app'

let store: Store<RootState> | null = null

export function bindAppStore(s: Store<RootState>) {
  store = s
}

export function isGlobalLoadingEnabled(): boolean {
  return store?.state.app.settings.enableGlobalLoading ?? true
}

export function startGlobalLoading() {
  if (!isGlobalLoadingEnabled()) return
  store?.commit('app/startLoading')
}

export function stopGlobalLoading() {
  store?.commit('app/stopLoading')
}

export function patchAppSettings(partial: Partial<NtestercAppSettings>) {
  store?.commit('app/patchSettings', partial)
}
