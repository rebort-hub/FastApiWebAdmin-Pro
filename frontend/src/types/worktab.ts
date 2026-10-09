export interface WorkTabItem {
  path: string
  title: string
  /** 路由 name，用于 keep-alive include */
  name?: string
  fixedTab?: boolean
  keepAlive?: boolean
}
