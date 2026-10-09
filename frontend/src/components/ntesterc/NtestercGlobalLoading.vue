<template>
  <div v-if="visible" class="ntesterc-global-loading">
    <a-spin size="large" :tip="tip" />
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import type { RootState } from '@/types/store'

defineOptions({ name: 'NtestercGlobalLoading' })

withDefaults(
  defineProps<{
    tip?: string
  }>(),
  {
    tip: '加载中...',
  },
)

const store = useStore<RootState>()
const visible = computed(() => store.getters['app/globalLoading'])
</script>

<style lang="scss" scoped>
.ntesterc-global-loading {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: all;
  background: rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(1px);
}
</style>
