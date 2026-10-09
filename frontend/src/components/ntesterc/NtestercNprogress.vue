<template>
  <div v-show="visible" class="ntesterc-nprogress">
    <div class="ntesterc-nprogress__bar" :style="{ width: `${percent}%` }" />
  </div>
</template>

<script lang="ts" setup>
import { useNtestercNprogress } from '@/composables/useNtestercNprogress'

defineOptions({ name: 'NtestercNprogress' })

const { visible, percent } = useNtestercNprogress()
</script>

<style lang="scss" scoped>
.ntesterc-nprogress {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  z-index: 2000;
  height: 2px;
  pointer-events: none;

  &__bar {
    height: 100%;
    background: var(--ntesterc-primary);
    box-shadow: 0 0 8px var(--ntesterc-primary);
    transition: width 0.16s ease;
  }
}
</style>
