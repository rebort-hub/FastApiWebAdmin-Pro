import request from '@/utils/axios'
import type { MenuRouteNode } from '@/types/menu'
import type { UserBasicInfo } from '@/types/store'

export function getCurrentUserInfo() {
  return request({
    url: '/api/system/user/current/info',
    method: 'get',
  })
}

export type CurrentUserPayload = UserBasicInfo & { menus: MenuRouteNode[] }

export function updateCurrentUserInfo(body: Record<string, unknown>) {
  return request({
    url: '/api/system/user/current/info/update',
    method: 'post',
    data: body,
  })
}

export function changeCurrentUserPassword(body: Record<string, unknown>) {
  return request({
    url: '/api/system/user/current/password/change',
    method: 'post',
    data: body,
  })
}

export function getUserList(parameter?: Record<string, unknown>) {
  return request({
    url: '/api/system/user/list',
    method: 'get',
    params: parameter,
  })
}

export function createUser(body: Record<string, unknown>) {
  return request({
    url: '/api/system/user/create',
    method: 'post',
    data: body,
  })
}

export function updateUser(body: Record<string, unknown>) {
  return request({
    url: '/api/system/user/update',
    method: 'post',
    data: body,
  })
}

export function deleteUser(parameter: Record<string, unknown>) {
  return request({
    url: '/api/system/user/delete',
    method: 'post',
    params: parameter,
  })
}

export function batchEnableUser(body: Record<string, unknown>) {
  return request({
    url: '/api/system/user/batch/enable',
    method: 'post',
    data: body,
  })
}

export function batchDisableUser(body: Record<string, unknown>) {
  return request({
    url: '/api/system/user/batch/disable',
    method: 'post',
    data: body,
  })
}
