/** 与后端 SuccessResponse / PaginationResponse 对齐 */
export interface ApiResult<T = unknown> {
  code: number
  message: string
  data: T
}

export interface PaginationResult<T = unknown> extends ApiResult<T[]> {
  total: number
  page: number
  page_size: number
  has_next: boolean
}
