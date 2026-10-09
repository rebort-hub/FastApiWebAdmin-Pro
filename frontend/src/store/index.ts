import { createStore } from 'vuex'
import user from './modules/user'
import app from './modules/app'
import worktab from './modules/worktab'
import type { RootState } from '@/types/store'

const store = createStore<RootState>({
  modules: {
    user,
    app,
    worktab,
  },
})

export default store
