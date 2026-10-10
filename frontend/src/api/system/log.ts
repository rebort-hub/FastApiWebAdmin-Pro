import request from '@/utils/axios'

export function getLogList(parameter?: Record<string, unknown>) {
  return request({
    url: '/api/system/log/list',
    method: 'get',
    params: parameter,
  })
}
