/** 后端菜单 / 动态路由节点 */
export interface MenuRouteNode {
  id: number
  name: string
  route_path: string
  route_name: string
  component_path?: string | null
  redirect?: string | null
  parent_id?: number | null
  icon?: string
  cache?: boolean
  hidden?: boolean
  order?: number
  children?: MenuRouteNode[]
}
