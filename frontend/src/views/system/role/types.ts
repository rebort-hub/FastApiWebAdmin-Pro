export interface searchDataType {
  name?: string
  available?: string
  [key: string]: unknown
}

export interface tableDataType {
  id?: number
  index?: number
  name?: string
  order?: number
  data_scope?: number
  available?: boolean
  description?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export interface permissionDataType {
  role_ids?: tableDataType['id'][]
  menu_ids?: permissionMenuType['id'][]
  data_scope?: number
  dept_ids?: number[]
  [key: string]: unknown
}

export interface permissionDeptType {
  id?: number
  name?: string
  parent_id?: number | null
  children?: permissionDeptType[]
}

export interface permissionMenuType {
  id?: number
  name?: string
  type?: number
  permission?: string
  parent_id?: number | null
  available?: boolean
  description?: string
  children?: permissionMenuType[]
}
