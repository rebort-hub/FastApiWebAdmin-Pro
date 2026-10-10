import type { Module } from 'vuex'
import { getCurrentUserInfo, type CurrentUserPayload } from '@/api/system/user'
import type { MenuRouteNode } from '@/types/menu'
import type { ApiResult } from '@/types/api'
import type { RootState, UserBasicInfo, UserState } from '@/types/store'

const user: Module<UserState, RootState> = {
  state: (): UserState => ({
    basicInfo: {},
    routeList: [],
    hasGetRoute: false,
  }),
  mutations: {
    setRoute(state, routers: MenuRouteNode[]) {
      state.routeList = routers
      state.hasGetRoute = true
    },
    setAvatar(state, avatar: string) {
      state.basicInfo.avatar = avatar
    },
  },
  actions: {
    getUserInfo({ commit, state }) {
      return new Promise<void>((resolve, reject) => {
        getCurrentUserInfo()
          .then((response) => {
            const result = response.data as ApiResult<CurrentUserPayload>
            const routers = result.data.menus
            const profile = { ...result.data } as UserBasicInfo & { menus?: MenuRouteNode[] }
            delete profile.menus
            commit('setRoute', routers)
            state.basicInfo = Object.assign(state.basicInfo || {}, profile)
            resolve()
          })
          .catch((error) => {
            console.log(error)
            reject(error)
          })
      })
    },

    clearUserInfo({ state }) {
      state.basicInfo = {}
      state.routeList = []
      state.hasGetRoute = false
    },
  },
}

export default user
