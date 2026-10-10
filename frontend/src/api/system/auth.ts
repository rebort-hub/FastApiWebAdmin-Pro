import request from '@/utils/axios'

export function login(body: URLSearchParams | Record<string, string | boolean | number>) {
  return request({
    url: '/api/system/auth/login',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: body,
  })
}

export function getNewToken(body: { refresh_token: string }) {
  return request({
    url: '/api/system/auth/token/refresh',
    method: 'post',
    data: body,
  })
}

export function getCaptcha() {
  return request({
    url: '/api/system/auth/captcha/get',
    method: 'post',
  })
}

export function sendEmailCode(data: { email: string }) {
  return request({
    url: '/api/system/auth/email/code',
    method: 'post',
    data,
  })
}

export function forgetPassword(data: Record<string, unknown>) {
  return request({
    url: '/api/system/auth/forget-password',
    method: 'post',
    data,
  })
}
