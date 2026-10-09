<template>
  <div class="ntesterc-page-header">
    <h1 v-if="title" class="ntesterc-page-header__title">{{ title }}</h1>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

defineOptions({ name: 'NtestercPageHeader' })

const route = useRoute()
const title = computed(() => route.meta.title?.toString() ?? '')
</script>

<style lang="scss" scoped>
.ntesterc-page-header {
  margin-bottom: 12px;

  &__title {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    line-height: 1.35;
    color: var(--ntesterc-text);
  }
}
</style>
