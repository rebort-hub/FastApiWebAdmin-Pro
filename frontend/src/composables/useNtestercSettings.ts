import { computed } from 'vue'
import { useStore } from 'vuex'
import type { RootState } from '@/types/store'
import type { NtestercAppSettings } from '@/types/app'
import { DEFAULT_APP_SETTINGS } from '@/types/app'

export function useNtestercSettings() {
  const store = useStore<RootState>()

  const settings = computed(() => store.state.app.settings)

  function patchSettings(partial: Partial<NtestercAppSettings>, persist = true) {
    store.commit(persist ? 'app/patchSettings' : 'app/previewSettings', partial)
  }

  function restoreSettings(next: NtestercAppSettings) {
    store.commit('app/restoreSettings', next)
  }

  function persistSettings() {
    store.commit('app/persistSettings')
  }

  function resetSettings() {
    store.commit('app/resetSettings')
  }

  return {
    settings,
    patchSettings,
    restoreSettings,
    persistSettings,
    resetSettings,
    defaults: DEFAULT_APP_SETTINGS,
  }
}
