import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import BasicLayout from '@/layouts/basicLayout.vue'
import Login from '@/views/system/auth/login.vue'
import ForgetPassword from '@/views/system/auth/forget-password.vue'
import storage from 'store'
import store from '@/store'
import { generator } from './generateRouter'
import { listToTree } from '@/utils/util'
import { doneNprogress, startNprogress } from '@/composables/useNtestercNprogress'

const publicRouteNames = new Set(['Login', 'ForgetPassword'])

function isPublicRoute(name: unknown): boolean {
  return typeof name === 'string' && publicRouteNames.has(name)
}

const routes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/forget-password', name: 'ForgetPassword', component: ForgetPassword },
  {
    path: '/:catchAll(.*)',
    name: '404',
    meta: { title: '404' },
    component: () => import('../views/exception/404.vue'),
  },
]

const rootRouter: RouteRecordRaw = {
  path: '/',
  name: 'Index',
  redirect: '/dashboard/workplace',
  component: BasicLayout,
  children: [
    {
      path: '/profile',
      name: 'Profile',
      meta: {
        title: '个人中心',
        keepAlive: true,
      },
      component: () => import('../views/current/profile.vue'),
    },
  ],
}

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (store.state.app.settings.showNprogress) startNprogress()
  const token = storage.get('Access-Token') as string | undefined

  if (!token && !isPublicRoute(to.name)) {
    return { name: 'Login' }
  }
  if (token && isPublicRoute(to.name)) {
    return { name: 'Index' }
  }
  if (token && !store.state.user.hasGetRoute) {
    return store.dispatch('getUserInfo').then(() => {
      const routersTree = listToTree(store.state.user.routeList)
      const routerMap = generator(routersTree)
      rootRouter.children = [...(rootRouter.children ?? []), ...routerMap]
      router.addRoute(rootRouter)
      return to.fullPath
    })
  }
})

router.afterEach(() => {
  doneNprogress()
})

export default router
