import type { MenuRouteNode } from './menu'

export interface UserBasicInfo {
  id?: number
  username?: string
  name?: string
  avatar?: string
  gender?: number
  mobile?: string
  email?: string
  dept_name?: string
  positions?: { id: number; name: string }[]
  roles?: { id: number; name: string }[]
  [key: string]: unknown
}

export interface UserState {
  basicInfo: UserBasicInfo
  routeList: MenuRouteNode[]
  hasGetRoute: boolean
}

import type { AppState } from './app'
import type { WorkTabState } from './worktabState'

export interface RootState {
  user: UserState
  app: AppState
  worktab: WorkTabState
}
