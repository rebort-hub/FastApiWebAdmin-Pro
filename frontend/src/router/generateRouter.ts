import type { RouteRecordRaw } from 'vue-router'
import type { MenuRouteNode } from '@/types/menu'

const modules = import.meta.glob('../views/**/*.vue')

/**
 * 将菜单树扁平为布局下的叶子路由，避免「目录节点无组件」导致嵌套 router-view 切换白屏。
 * 侧边栏仍使用原始菜单树，不受影响。
 */
export const generator = (routers: MenuRouteNode[]): RouteRecordRaw[] => {
  const routes: RouteRecordRaw[] = []

  const walk = (nodes: MenuRouteNode[]) => {
    for (const item of nodes) {
      const hasChildren = Boolean(item.children?.length)

      if (hasChildren) {
        if (item.redirect) {
          routes.push({
            path: item.route_path,
            name: item.route_name,
            redirect: item.redirect,
            meta: {
              title: item.name,
              icon: item.icon || undefined,
              hidden: item.hidden,
              order: item.order,
            },
          })
        }
        walk(item.children!)
        continue
      }

      if (!item.component_path) continue

      const viewLoader = modules[`../views/${item.component_path}.vue`]
      if (!viewLoader) continue

      routes.push({
        path: item.route_path,
        name: item.route_name,
        component: viewLoader,
        meta: {
          title: item.name,
          icon: item.icon || undefined,
          keepAlive: item.cache,
          hidden: item.hidden,
          order: item.order,
        },
      })
    }
  }

  walk(routers)
  return routes
}
