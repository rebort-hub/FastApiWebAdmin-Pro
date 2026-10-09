export interface searchDataType {
  request_path?: string
  creator?: number
  creator_name?: string
  date_range?: [string, string]
  [key: string]: unknown
}

export interface tableDataType {
  id?: number
  index?: number
  request_path?: string
  request_method?: string
  request_ip?: string
  request_browser?: string
  request_os?: string
  response_code?: number
  request_payload: string
  response_json?: string
  creator?: creatorTableDataType
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export interface searchCreatorDataType {
  name?: string
  available?: string
  [key: string]: unknown
}

export interface creatorTableDataType {
  id?: number
  name?: string
  available?: string
  description?: string
}
