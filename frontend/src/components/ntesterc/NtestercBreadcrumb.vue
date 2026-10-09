<template>
  <a-breadcrumb class="ntesterc-breadcrumb">
    <a-breadcrumb-item v-for="(item, index) in items" :key="item.path + index">
      <router-link v-if="index < items.length - 1" :to="item.path">{{ item.title }}</router-link>
      <span v-else>{{ item.title }}</span>
    </a-breadcrumb-item>
  </a-breadcrumb>
</template>

<script lang="ts" setup>
defineOptions({ name: 'NtestercBreadcrumb' })

export interface NtestercBreadcrumbItem {
  path: string
  title: string
}

defineProps<{
  items: NtestercBreadcrumbItem[]
}>()
</script>

<style lang="scss" scoped>
.ntesterc-breadcrumb {
  font-size: 13px;

  :deep(.ant-breadcrumb-link),
  :deep(a) {
    color: var(--ntesterc-text-secondary);
  }

  :deep(li:last-child) {
    color: var(--ntesterc-text);
    font-weight: 500;
  }
}
</style>
