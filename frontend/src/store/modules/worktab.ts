import type { Module } from 'vuex'
import type { RootState } from '@/types/store'
import type { WorkTabState } from '@/types/worktabState'
import type { WorkTabItem } from '@/types/worktab'

const HOME_PATH = '/dashboard/workplace'

const worktab: Module<WorkTabState, RootState> = {
  namespaced: true,
  state: (): WorkTabState => ({
    opened: [
      {
        path: HOME_PATH,
        title: '工作台',
        name: 'Workplace',
        fixedTab: true,
        keepAlive: true,
      },
    ],
    activePath: HOME_PATH,
  }),
  getters: {
    keepAliveInclude: (state) =>
      state.opened
        .filter((t) => t.keepAlive && t.name)
        .map((t) => t.name as string),
  },
  mutations: {
    setActivePath(state, path: string) {
      state.activePath = path
    },
    openTab(state, tab: WorkTabItem) {
      const idx = state.opened.findIndex((t) => t.path === tab.path)
      if (idx === -1) {
        const insertAt = tab.fixedTab ? 0 : state.opened.length
        state.opened.splice(insertAt, 0, tab)
      } else {
        state.opened[idx] = { ...state.opened[idx], ...tab }
      }
      state.activePath = tab.path
    },
    removeTab(state, path: string) {
      const tab = state.opened.find((t) => t.path === path)
      if (!tab || tab.fixedTab) return
      state.opened = state.opened.filter((t) => t.path !== path)
    },
    removeOtherTabs(state, path: string) {
      state.opened = state.opened.filter((t) => t.fixedTab || t.path === path)
      state.activePath = path
    },
    removeLeftTabs(state, path: string) {
      const index = state.opened.findIndex((t) => t.path === path)
      if (index <= 0) return
      state.opened = state.opened.filter((t, i) => t.fixedTab || i >= index)
    },
    removeRightTabs(state, path: string) {
      const index = state.opened.findIndex((t) => t.path === path)
      if (index < 0) return
      state.opened = state.opened.filter((t, i) => t.fixedTab || i <= index)
    },
    removeAllTabs(state) {
      state.opened = state.opened.filter((t) => t.fixedTab)
      state.activePath = state.opened[0]?.path ?? HOME_PATH
    },
  },
  actions: {
    openTab({ commit }, tab: WorkTabItem) {
      commit('openTab', tab)
    },
    closeTab({ commit, state, dispatch }, path: string) {
      commit('removeTab', path)
      if (state.activePath === path) {
        const last = state.opened[state.opened.length - 1]
        return last?.path
      }
      return state.activePath
    },
  },
}

export default worktab
