import request from '@/utils/axios'

export function getMenuList() {
  return request({
    url: '/api/system/menu/list',
    method: 'get',
  })
}

export function getMenuOptions() {
  return request({
    url: '/api/system/menu/options',
    method: 'get',
  })
}

export function createMenu(body: Record<string, unknown>) {
  return request({
    url: '/api/system/menu/create',
    method: 'post',
    data: body,
  })
}

export function updateMenu(body: Record<string, unknown>) {
  return request({
    url: '/api/system/menu/update',
    method: 'post',
    data: body,
  })
}

export function deleteMenu(parameter: Record<string, unknown>) {
  return request({
    url: '/api/system/menu/delete',
    method: 'post',
    params: parameter,
  })
}

export function batchEnableMenu(body: Record<string, unknown>) {
  return request({
    url: '/api/system/menu/batch/enable',
    method: 'post',
    data: body,
  })
}

export function batchDisableMenu(body: Record<string, unknown>) {
  return request({
    url: '/api/system/menu/batch/disable',
    method: 'post',
    data: body,
  })
}
