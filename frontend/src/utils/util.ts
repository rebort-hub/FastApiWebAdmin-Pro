import storage from 'store'
import type { TreeNodeLike } from '@/types/tree'

export function timeFix(): string {
  const time = new Date()
  const hour = time.getHours()
  return hour < 9
    ? '早上好'
    : hour <= 11
      ? '上午好'
      : hour <= 13
        ? '中午好'
        : hour < 20
          ? '下午好'
          : '晚上好'
}

export function getRangeDate(startDate: string | Date, endDate: string | Date): string[] {
  const targetArr: string[] = []
  const start = new Date(startDate)
  const end = new Date(endDate)
  const startDateInfo = {
    year: start.getFullYear(),
    month: start.getMonth() + 1,
    day: start.getDate(),
  }
  const endDateInfo = {
    year: end.getFullYear(),
    month: end.getMonth() + 1,
    day: end.getDate(),
  }
  if (startDateInfo.year === endDateInfo.year) {
    if (startDateInfo.month !== endDateInfo.month) {
      const startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate()
      const endNum = startMax - startDateInfo.day + endDateInfo.day
      for (let i = startDateInfo.day; i <= startDateInfo.day + endNum; i++) {
        if (i > startMax) {
          targetArr.push(
            `${endDateInfo.year}-${endDateInfo.month < 10 ? '0' + endDateInfo.month : endDateInfo.month}-${i - startMax < 10 ? '0' + (i - startMax) : i - startMax}`,
          )
        } else {
          targetArr.push(
            `${startDateInfo.year}-${startDateInfo.month < 10 ? '0' + startDateInfo.month : startDateInfo.month}-${i < 10 ? '0' + i : i}`,
          )
        }
      }
    } else {
      for (let i = startDateInfo.day; i <= endDateInfo.day; i++) {
        targetArr.push(
          `${startDateInfo.year}-${startDateInfo.month < 10 ? '0' + startDateInfo.month : startDateInfo.month}-${i < 10 ? '0' + i : i}`,
        )
      }
    }
  } else {
    const startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate()
    const endNum = startMax - startDateInfo.day + endDateInfo.day
    for (let i = startDateInfo.day; i <= startDateInfo.day + endNum; i++) {
      if (i > startMax) {
        targetArr.push(
          `${endDateInfo.year}-${endDateInfo.month < 10 ? '0' + endDateInfo.month : endDateInfo.month}-${i - startMax < 10 ? '0' + (i - startMax) : i - startMax}`,
        )
      } else {
        targetArr.push(
          `${startDateInfo.year}-${startDateInfo.month < 10 ? '0' + startDateInfo.month : startDateInfo.month}-${i < 10 ? '0' + i : i}`,
        )
      }
    }
  }

  return targetArr
}

export function save_token(access_token: string, refresh_token: string, expires_in: number): void {
  storage.set('Access-Token', access_token, new Date().getTime() + expires_in)
  storage.set('Refresh-Token', refresh_token)
}

export function listToTree<T extends TreeNodeLike>(list: T[]): T[] {
  const resultList = list.filter((item) => {
    const children = list.filter((child) => item.id === child.parent_id) as T[]
    if (children.length > 0) {
      ;(item as TreeNodeLike).children = children
    }
    return item.parent_id === null || item.parent_id === undefined
  })
  return cloneDeep(resultList)
}

export function cloneDeep<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj)) as T
}

export function isEmpty(obj: unknown): boolean {
  return obj === undefined || obj === null || obj === ''
}
