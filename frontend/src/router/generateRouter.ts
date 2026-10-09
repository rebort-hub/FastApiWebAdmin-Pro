import type { RouteRecordRaw } from 'vue-router'
import type { MenuRouteNode } from '@/types/menu'

const modules = import.meta.glob('../views/**/*.vue')

export const generator = (routers: MenuRouteNode[]): RouteRecordRaw[] => {
  return routers.map((item) => {
    const componentPath = item.component_path
      ? modules[`../views/${item.component_path}.vue`]
      : undefined

    const currentRouter: RouteRecordRaw = {
      path: item.route_path,
      name: item.route_name,
      component: componentPath as RouteRecordRaw['component'],
      redirect: item.redirect || undefined,
      meta: {
        title: item.name,
        icon: item.icon || undefined,
        keepAlive: item.cache,
        hidden: item.hidden,
        order: item.order,
      },
      children: undefined,
    }

    if (item.children && item.children.length > 0) {
      currentRouter.children = generator(item.children)
    }
    return currentRouter
  })
}
