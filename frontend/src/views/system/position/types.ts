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
  available?: boolean
  description?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}
