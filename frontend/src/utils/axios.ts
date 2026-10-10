import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'
import storage from 'store'
import router from '@/router'
import { getNewToken } from '@/api/system/auth'
import { save_token } from './util'
import notification from 'ant-design-vue/es/notification'
import type { ApiResult } from '@/types/api'
import { startGlobalLoading, stopGlobalLoading } from '@/utils/appStoreBridge'

const apiUrl = import.meta.env.VITE_API_BASE_URL

interface ErrorBody {
  code?: number
  message?: string
}

const request = axios.create({
  baseURL: apiUrl,
  timeout: 10000,
})

const errorHandler = async (error: AxiosError<ErrorBody>) => {
  if (error.config && !error.config.headers?.['X-Skip-Loading']) {
    stopGlobalLoading()
  }
  if (!error.response) {
    return Promise.reject(error)
  }

  const data = error.response.data
  const access_token = storage.get('Access-Token') as string | undefined

  if (data.code === 403) {
    storage.remove('Access-Token')
    storage.remove('Refresh-Token')

    notification.error({
      message: '错误',
      description: data.message,
    })
    router.push('/login')
    return Promise.reject(error)
  }

  if (data.code === 401) {
    if (!access_token) {
      notification.error({
        message: '错误',
        description: data.message,
      })
      router.push('/login')
      return Promise.reject(error)
    }

    const refresh_token = storage.get('Refresh-Token') as string
    storage.remove('Access-Token')
    storage.remove('Refresh-Token')

    return getNewToken({ refresh_token })
      .then((response) => {
        const result = response.data as ApiResult<{
          access_token: string
          refresh_token: string
          expires_in: number
        }>
        if (result.code === 200) {
          save_token(result.data.access_token, result.data.refresh_token, result.data.expires_in)
          const config = error.response?.config as InternalAxiosRequestConfig
          return request(config)
        }

        notification.error({
          message: '错误',
          description: result.message,
        })
        router.push('/login')
        return Promise.reject(error)
      })
      .catch((err) => {
        notification.error({
          message: '错误',
          description: data.message,
        })
        return Promise.reject(err)
      })
  }

  notification.error({
    message: '错误',
    description: data.message,
  })
  return Promise.reject(error)
}

request.interceptors.request.use((config) => {
  const token = storage.get('Access-Token') as string | undefined
  if (token) {
    config.headers.Authorization = 'Bearer ' + token
  }
  if (!config.headers?.['X-Skip-Loading']) {
    startGlobalLoading()
  }
  return config
}, errorHandler)

request.interceptors.response.use((response) => {
  if (!response.config.headers?.['X-Skip-Loading']) {
    stopGlobalLoading()
  }
  const body = response.data as ApiResult
  if (body.code !== 200) {
    notification.error({
      message: '错误',
      description: body.message,
    })
    return Promise.reject(response)
  }
  return response
}, errorHandler)

export default request
