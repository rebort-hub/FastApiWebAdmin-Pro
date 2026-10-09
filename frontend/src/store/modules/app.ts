import type { Module } from 'vuex'
import { DEFAULT_APP_SETTINGS, type AppState, type NtestercAppSettings } from '@/types/app'
import type { RootState } from '@/types/store'
import { setPrimaryColor, setTheme } from '@/composables/useNtestercTheme'

const SETTINGS_KEY = 'ntesterc-app-settings'

function loadSettings(): NtestercAppSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (raw) {
      return { ...DEFAULT_APP_SETTINGS, ...JSON.parse(raw) }
    }
  } catch {
    /* ignore */
  }
  return { ...DEFAULT_APP_SETTINGS }
}

function saveSettings(settings: NtestercAppSettings) {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
}

function applyRuntime(settings: NtestercAppSettings) {
  setTheme(settings.themeMode)
  setPrimaryColor(settings.primaryColor)
  const html = document.documentElement
  html.setAttribute('data-menu-layout', settings.menuLayout)
  html.setAttribute('data-menu-style', settings.menuStyle)
  html.setAttribute('data-box-mode', settings.boxStyle)
  html.setAttribute('data-container-width', settings.containerWidth)
  html.style.setProperty(
    '--ntesterc-container-width',
    settings.containerWidth === 'full' ? '100%' : `${settings.containerFixedWidth}px`,
  )
}

const initialSettings = loadSettings()
applyRuntime(initialSettings)

function mergeSettings(state: AppState, partial: Partial<NtestercAppSettings>, persist: boolean) {
  state.settings = { ...state.settings, ...partial }
  applyRuntime(state.settings)
  if (persist) saveSettings(state.settings)
}

const app: Module<AppState, RootState> = {
  namespaced: true,
  state: (): AppState => ({
    settings: initialSettings,
    loadingCount: 0,
  }),
  getters: {
    globalLoading: (state) => state.loadingCount > 0,
  },
  mutations: {
    patchSettings(state, partial: Partial<NtestercAppSettings>) {
      mergeSettings(state, partial, true)
    },
    previewSettings(state, partial: Partial<NtestercAppSettings>) {
      mergeSettings(state, partial, false)
    },
    restoreSettings(state, next: NtestercAppSettings) {
      state.settings = { ...DEFAULT_APP_SETTINGS, ...next }
      applyRuntime(state.settings)
    },
    persistSettings(state) {
      saveSettings(state.settings)
    },
    resetSettings(state) {
      state.settings = { ...DEFAULT_APP_SETTINGS }
      saveSettings(state.settings)
      applyRuntime(state.settings)
    },
    startLoading(state) {
      state.loadingCount += 1
    },
    stopLoading(state) {
      state.loadingCount = Math.max(0, state.loadingCount - 1)
    },
  },
}

export default app
