<template>
  <div class="ntesterc-pagination" :class="`ntesterc-pagination--${align}`">
    <a-pagination
      :current="current"
      :page-size="pageSize"
      :total="total"
      :show-size-changer="showSizeChanger"
      :show-quick-jumper="showQuickJumper"
      :page-size-options="pageSizeOptions"
      :show-total="resolvedShowTotal"
      @change="onChange"
      @showSizeChange="onShowSizeChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

defineOptions({ name: 'NtestercPagination' })

const props = withDefaults(
  defineProps<{
    current?: number
    pageSize?: number
    total?: number
    showSizeChanger?: boolean
    showQuickJumper?: boolean
    pageSizeOptions?: string[]
    align?: 'left' | 'center' | 'right'
    showTotal?: (total: number, range: [number, number]) => string
  }>(),
  {
    current: 1,
    pageSize: 10,
    total: 0,
    showSizeChanger: true,
    showQuickJumper: true,
    pageSizeOptions: () => ['10', '20', '50', '100'],
    align: 'right',
  },
)

const emit = defineEmits<{
  change: [page: number, pageSize: number]
}>()

const defaultShowTotal = (total: number, range: [number, number]) =>
  `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`

const resolvedShowTotal = computed(() => props.showTotal ?? defaultShowTotal)

function onChange(page: number, pageSize: number) {
  emit('change', page, pageSize)
}

function onShowSizeChange(current: number, size: number) {
  emit('change', current, size)
}
</script>

<style lang="scss" scoped>
$pg-height: 32px;

.ntesterc-pagination {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  width: 100%;
  min-height: $pg-height;
  padding: 6px 0 10px;
  overflow: visible;

  &--left {
    justify-content: flex-start;
  }

  &--center {
    justify-content: center;
  }

  &--right {
    justify-content: flex-end;
  }

  :deep(.ant-pagination) {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    justify-content: flex-end;
    margin: 0;
  }

  :deep(.ant-pagination-total-text) {
    display: inline-flex;
    align-items: center;
    height: $pg-height;
    margin-inline-end: 4px;
    line-height: $pg-height;
    color: var(--ntesterc-text-secondary);
    font-size: 13px;
  }

  :deep(.ant-pagination-prev),
  :deep(.ant-pagination-next),
  :deep(.ant-pagination-item) {
    height: $pg-height;
    min-width: $pg-height;
    margin-inline-end: 0;
    line-height: calc($pg-height - 2px);
    border-radius: 6px;
  }

  :deep(.ant-pagination-item) {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-color: var(--ntesterc-border);
    background: transparent;

    a {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      padding: 0;
      color: var(--ntesterc-text);
    }
  }

  :deep(.ant-pagination-item-active) {
    font-weight: 500;
    border-color: var(--ntesterc-primary, #1677ff);
    background: transparent;

    a {
      color: var(--ntesterc-primary, #1677ff);
    }
  }

  :deep(.ant-pagination-prev .ant-pagination-item-link),
  :deep(.ant-pagination-next .ant-pagination-item-link) {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    border-radius: 6px;
    border-color: var(--ntesterc-border);
    background: transparent;
  }

  :deep(.ant-pagination-disabled .ant-pagination-item-link) {
    color: var(--ntesterc-text-secondary);
  }

  :deep(.ant-pagination-options) {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    margin-inline-start: 0;
  }

  :deep(.ant-pagination-options-size-changer) {
    height: $pg-height;

    .ant-select-selector {
      display: flex;
      align-items: center;
      height: $pg-height !important;
      padding: 0 11px !important;
      border-radius: 6px !important;
      border-color: var(--ntesterc-border) !important;
    }

    .ant-select-selection-item {
      line-height: calc($pg-height - 2px) !important;
    }
  }

  :deep(.ant-pagination-options-quick-jumper) {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    height: $pg-height;
    margin-inline-start: 0;
    line-height: $pg-height;
    color: var(--ntesterc-text-secondary);
    font-size: 13px;

    input {
      box-sizing: border-box;
      width: 48px;
      height: $pg-height;
      padding: 0 8px;
      text-align: center;
      border-radius: 6px;
      border-color: var(--ntesterc-border);
    }
  }
}
</style>
