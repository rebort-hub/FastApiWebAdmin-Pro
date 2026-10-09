export interface treeDataType {
  id?: number
  name?: string
  order?: number
  parent_id?: number | null
  available?: boolean
  description?: string
  children?: treeDataType[]
  [key: string]: unknown
}
