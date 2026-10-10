import type { RouteRecordRaw } from 'vue-router'
import type { MenuRouteNode } from '@/types/menu'

const modules = import.meta.glob('../views/**/*.vue')


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
