import { computed, ref, watch } from 'vue'
import { theme } from 'ant-design-vue'
import type { ThemeConfig } from 'ant-design-vue/es/config-provider/context'

const STORAGE_KEY = 'ntesterc-theme-mode'

export type NtestercThemeMode = 'light' | 'dark' | 'auto'
export type NtestercResolvedTheme = 'light' | 'dark'

const themeMode = ref<NtestercThemeMode>(readStoredMode())
const resolvedTheme = ref<NtestercResolvedTheme>(resolveTheme(themeMode.value))
const primaryColor = ref('#1677ff')

function readStoredMode(): NtestercThemeMode {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'light' || stored === 'dark' || stored === 'auto') return stored
  return 'light'
}

function getSystemTheme(): NtestercResolvedTheme {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function resolveTheme(mode: NtestercThemeMode): NtestercResolvedTheme {
  return mode === 'auto' ? getSystemTheme() : mode
}

function applyDocumentTheme(mode: NtestercResolvedTheme) {
  document.documentElement.setAttribute('data-ntesterc-theme', mode)
}

function applyResolvedTheme() {
  resolvedTheme.value = resolveTheme(themeMode.value)
  applyDocumentTheme(resolvedTheme.value)
}

applyResolvedTheme()

const media = window.matchMedia('(prefers-color-scheme: dark)')
const onSystemThemeChange = () => {
  if (themeMode.value === 'auto') applyResolvedTheme()
}
media.addEventListener('change', onSystemThemeChange)

watch(
  themeMode,
  (mode) => {
    localStorage.setItem(STORAGE_KEY, mode)
    applyResolvedTheme()
  },
  { immediate: true },
)

export function setPrimaryColor(color: string) {
  primaryColor.value = color
  document.documentElement.style.setProperty('--ntesterc-primary', color)
}

setPrimaryColor(primaryColor.value)

export function setTheme(mode: NtestercThemeMode) {
  themeMode.value = mode
}

export function useNtestercTheme() {
  const isDark = computed(() => resolvedTheme.value === 'dark')

  const antdTheme = computed<ThemeConfig>(() => {
    const baseToken = {
      colorPrimary: primaryColor.value,
      borderRadius: 8,
      wireframe: false,
    }

    if (!isDark.value) {
      return {
        algorithm: theme.defaultAlgorithm,
        token: baseToken,
      }
    }

    return {
      algorithm: theme.darkAlgorithm,
      token: {
        ...baseToken,
        colorBgBase: '#000000',
        colorBgLayout: '#000000',
        colorBgContainer: '#141414',
        colorBgElevated: '#1f1f1f',
        colorBorder: 'rgba(255, 255, 255, 0.08)',
        colorBorderSecondary: 'rgba(255, 255, 255, 0.06)',
        colorText: 'rgba(255, 255, 255, 0.85)',
        colorTextSecondary: 'rgba(255, 255, 255, 0.45)',
        colorFillAlter: '#1a1a1a',
        colorFillSecondary: 'rgba(255, 255, 255, 0.08)',
      },
    }
  })

  function toggleTheme() {
    themeMode.value = isDark.value ? 'light' : 'dark'
  }

  function syncPrimaryFromSettings(color: string) {
    setPrimaryColor(color)
  }

  return {
    themeMode,
    resolvedTheme,
    primaryColor,
    isDark,
    antdTheme,
    toggleTheme,
    setTheme,
    setPrimaryColor,
    syncPrimaryFromSettings,
  }
}
