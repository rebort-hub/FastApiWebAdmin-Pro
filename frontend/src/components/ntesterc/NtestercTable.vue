<template>
  <div class="ntesterc-table" :class="{ 'ntesterc-table--striped': striped }">
    <a-table v-bind="tableBind" @change="onTableChange">
      <template v-for="(_, name) in $slots" #[name]="slotData">
        <slot :name="name" v-bind="slotData || {}" />
      </template>
    </a-table>
    <NtestercPagination
      v-if="showFooterPagination"
      class="ntesterc-table__pagination"
      :current="footerPagination.current"
      :page-size="footerPagination.pageSize"
      :total="footerPagination.total"
      :show-size-changer="footerPagination.showSizeChanger"
      :show-quick-jumper="footerPagination.showQuickJumper"
      :page-size-options="footerPagination.pageSizeOptions"
      :show-total="footerPagination.showTotal"
      :align="footerPagination.align"
      @change="onFooterPageChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, useAttrs } from 'vue'
import type { TablePaginationConfig, TableProps } from 'ant-design-vue'
import NtestercPagination from './NtestercPagination.vue'

withDefaults(
  defineProps<{
    striped?: boolean
  }>(),
  {
    striped: true,
  },
)

defineOptions({ name: 'NtestercTable', inheritAttrs: false })

const attrs = useAttrs()

type ChangeHandler = TableProps['onChange']

const paginationProp = computed(
  () => attrs.pagination as TablePaginationConfig | false | undefined,
)

const showFooterPagination = computed(() => paginationProp.value !== false && paginationProp.value != null)

const tableBind = computed(() => {
  const { onChange: _onChange, ...rest } = attrs as Record<string, unknown>
  return {
    ...rest,
    pagination: paginationProp.value === false ? false : paginationProp.value,
  }
})

function resolveDataLength(): number {
  const data = (attrs['data-source'] ?? attrs.dataSource) as unknown[] | undefined
  return Array.isArray(data) ? data.length : 0
}

const footerPagination = computed(() => {
  const p = paginationProp.value
  if (!p || p === false) {
    return {
      current: 1,
      pageSize: 10,
      total: 0,
      showSizeChanger: true,
      showQuickJumper: true,
      pageSizeOptions: ['10', '20', '50', '100'],
      showTotal: undefined as TablePaginationConfig['showTotal'],
      align: 'right' as const,
    }
  }
  return {
    current: p.current ?? 1,
    pageSize: p.pageSize ?? 10,
    total: p.total ?? resolveDataLength(),
    showSizeChanger: p.showSizeChanger ?? true,
    showQuickJumper: p.showQuickJumper ?? true,
    pageSizeOptions: (p.pageSizeOptions ?? ['10', '20', '50', '100']).map(String),
    showTotal: p.showTotal,
    align: 'right' as const,
  }
})

function onTableChange(
  pag: TablePaginationConfig,
  filters: Record<string, unknown>,
  sorter: unknown,
  extra?: unknown,
) {
  const handler = attrs.onChange as ChangeHandler | undefined
  handler?.(pag, filters, sorter, extra)
}

function onFooterPageChange(page: number, pageSize: number) {
  const p = paginationProp.value
  if (!p || p === false) return
  const pag: TablePaginationConfig = {
    ...p,
    current: page,
    pageSize,
    total: p.total ?? resolveDataLength(),
  }
  onTableChange(pag, {}, {}, { action: 'paginate' })
}
</script>

<style lang="scss" scoped>
.ntesterc-table {
  display: flex;
  flex-direction: column;

  :deep(.ant-table) {
    overflow: hidden;
    background: var(--ntesterc-card-bg);
    border-radius: 10px;
  }

  :deep(.ant-table-thead > tr > th) {
    font-weight: 600;
    color: var(--ntesterc-text);
    background: var(--ntesterc-table-header-bg) !important;
    border-bottom: 1px solid var(--ntesterc-border) !important;
  }

  :deep(.ant-table-tbody > tr > td) {
    border-bottom: 1px solid var(--ntesterc-border);
    transition: background 0.15s ease;
  }

  &--striped {
    :deep(.ant-table-tbody > tr > td) {
      background: var(--ntesterc-table-row-bg);
    }

    :deep(.ant-table-tbody > tr:nth-child(even) > td) {
      background: var(--ntesterc-table-stripe-bg);
    }
  }

  :deep(.ant-table-tbody > tr:hover > td) {
    background: var(--ntesterc-menu-hover) !important;
  }

  :deep(.ant-table-cell) {
    padding: 12px 16px !important;
    vertical-align: middle;
  }

  :deep(.ant-table-body > table > .ant-table-tbody > tr) {
    height: auto;
  }

  :deep(.ant-table-thead > tr > th.ant-table-cell-fix-left),
  :deep(.ant-table-thead > tr > th.ant-table-cell-fix-right) {
    background: var(--ntesterc-table-header-bg) !important;
  }

  :deep(.ant-table-tbody > tr > td.ant-table-cell-fix-left),
  :deep(.ant-table-tbody > tr > td.ant-table-cell-fix-right) {
    background: var(--ntesterc-table-row-bg) !important;
  }

  &--striped {
    :deep(.ant-table-tbody > tr:nth-child(even) > td.ant-table-cell-fix-left),
    :deep(.ant-table-tbody > tr:nth-child(even) > td.ant-table-cell-fix-right) {
      background: var(--ntesterc-table-stripe-bg) !important;
    }
  }

  :deep(.ant-table-tbody > tr:hover > td.ant-table-cell-fix-left),
  :deep(.ant-table-tbody > tr:hover > td.ant-table-cell-fix-right) {
    background: var(--ntesterc-menu-hover) !important;
  }

  :deep(.ant-table-pagination) {
    display: none !important;
  }

  &__pagination {
    flex-shrink: 0;
    margin-top: 16px;
    margin-bottom: 4px;
    padding: 8px 4px 12px;
    overflow: visible;
  }
}
</style>
