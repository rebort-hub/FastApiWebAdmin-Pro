import request from '@/utils/axios'

export const STORAGE_TYPE_LABELS: Record<string, string> = {
  local: '本地存储',
  aliyun_oss: '阿里云 OSS',
  tencent_cos: '腾讯云 COS',
  qiniu: '七牛云',
  minio: 'MinIO',
}

export function uploadFile(formData: FormData) {
  return request({
    url: '/api/system/file/upload',
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    data: formData,
  })
}

export function getFileList({
  page,
  page_size,
  name,
  storage_type,
}: {
  page: number
  page_size: number
  name?: string
  storage_type?: string
}) {
  return request({
    url: '/api/system/file/list',
    method: 'post',
    params: { page, page_size },
    data: { name, storage_type },
  })
}

export function getFileStatistics() {
  return request({ url: '/api/system/file/statistics', method: 'get' })
}

export function getStorageConfig() {
  return request({ url: '/api/system/file/storage-config', method: 'get' })
}

export function deleteFile(data: { id: number }) {
  return request({ url: '/api/system/file/deleted', method: 'post', data })
}

export function deleteFileList(data: { ids: number[] }) {
  return request({ url: '/api/system/file/deleteList', method: 'post', data })
}

export function getFileDownloadUrl(fileId: number | string) {
  const base = import.meta.env.VITE_API_BASE_URL || ''
  return `${base}/api/system/file/download/${fileId}`
}
