import type { NtestercThemeMode } from '@/composables/useNtestercTheme'

export type NtestercMenuLayout = 'vertical' | 'horizontal' | 'mixed' | 'dual'
export type NtestercMenuStyle = 'simple' | 'card' | 'outline' | 'immersive' | 'glass'
export type NtestercBoxStyle = 'border' | 'shadow'
export type NtestercContainerWidth = 'full' | 'fixed'
export type NtestercPageTransition = 'fade' | 'slide-left' | 'slide-bottom' | 'slide-top'

export interface NtestercAppSettings {
  themeMode: NtestercThemeMode
  primaryColor: string
  menuLayout: NtestercMenuLayout
  menuStyle: NtestercMenuStyle
  boxStyle: NtestercBoxStyle
  containerWidth: NtestercContainerWidth
  containerFixedWidth: number
  enablePageAnimation: boolean
  showBreadcrumb: boolean
  pageTransition: NtestercPageTransition
  showNprogress: boolean
  showWorkTab: boolean
  enableGlobalLoading: boolean
}

export const DEFAULT_APP_SETTINGS: NtestercAppSettings = {
  themeMode: 'light',
  primaryColor: '#1677ff',
  menuLayout: 'vertical',
  menuStyle: 'simple',
  boxStyle: 'border',
  containerWidth: 'full',
  containerFixedWidth: 1200,
  enablePageAnimation: true,
  showBreadcrumb: true,
  pageTransition: 'fade',
  showNprogress: true,
  showWorkTab: false,
  enableGlobalLoading: true,
}

export const NTESTERC_PRESET_COLORS = [
  '#1677ff',
  '#13c2c2',
  '#52c41a',
  '#722ed1',
  '#fa8c16',
  '#f5222d',
  '#2f54eb',
]

export const NTESTERC_PAGE_TRANSITIONS: { value: NtestercPageTransition; label: string }[] = [
  { value: 'fade', label: '渐入' },
  { value: 'slide-left', label: '左滑' },
  { value: 'slide-bottom', label: '下滑' },
  { value: 'slide-top', label: '上滑' },
]

export interface AppState {
  settings: NtestercAppSettings
  loadingCount: number
}
