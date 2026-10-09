<template>
  <a-card class="ntesterc-table-card" :bordered="false">
    <template v-if="title || $slots.extra" #title>
      <div class="ntesterc-table-card__head">
        <span v-if="title" class="ntesterc-table-card__title">{{ title }}</span>
        <slot name="title" />
      </div>
    </template>
    <template v-if="$slots.extra" #extra>
      <slot name="extra" />
    </template>
    <div class="ntesterc-table-card__body">
      <slot />
    </div>
  </a-card>
</template>

<script lang="ts" setup>
defineOptions({ name: 'NtestercTableCard' })

defineProps<{
  title?: string
}>()
</script>

<style lang="scss" scoped>
.ntesterc-table-card {
  background: var(--ntesterc-card-bg);
  border: 1px solid var(--ntesterc-border);
  border-radius: 12px;
  box-shadow: var(--ntesterc-shadow);

  :deep(.ant-card-head) {
    min-height: 56px;
    padding: 0 20px;
    border-bottom: 1px solid var(--ntesterc-border);
  }

  :deep(.ant-card-head-title) {
    padding: 16px 0;
  }

  :deep(.ant-card-extra) {
    padding: 12px 0;
  }

  :deep(.ant-card-body) {
    padding: 16px 20px 24px;
  }

  &__body {
    overflow: visible;
  }

  &__title {
    font-size: 16px;
    font-weight: 600;
    color: var(--ntesterc-text);
  }

  &__head {
    display: flex;
    gap: 8px;
    align-items: center;
  }
}
</style>
