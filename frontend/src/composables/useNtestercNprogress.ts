import { ref } from 'vue'

const visible = ref(false)
const percent = ref(0)
let timer: number | undefined

export function startNprogress() {
  visible.value = true
  percent.value = 12
  window.clearInterval(timer)
  timer = window.setInterval(() => {
    percent.value = Math.min(percent.value + 8 + Math.random() * 10, 92)
  }, 180)
}

export function doneNprogress() {
  window.clearInterval(timer)
  percent.value = 100
  window.setTimeout(() => {
    visible.value = false
    percent.value = 0
  }, 220)
}

export function useNtestercNprogress() {
  return { visible, percent }
}
