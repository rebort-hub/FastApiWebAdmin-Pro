<template>
  <div>
    <page-header />
    <div class="table-search-wrapper">
      <a-card :bordered="false">
        <a-row :gutter="16" v-if="storageConfig.storage_type">
          <a-col :span="6">
            <a-statistic title="文件总数" :value="statistics.total_count || 0" />
          </a-col>
          <a-col :span="6">
            <a-statistic title="总大小" :value="formatSize(statistics.total_size_kb)" />
          </a-col>
          <a-col :span="6">
            <a-statistic title="当前存储" :value="storageConfig.storage_label || storageConfig.storage_type" />
          </a-col>
          <a-col :span="6">
            <a-statistic title="单文件上限" :value="`${storageConfig.max_size || 0} MB`" />
          </a-col>
        </a-row>
        <a-divider />
        <a-space wrap>
          <a-upload
            :show-upload-list="false"
            :custom-request="handleUpload"
            :multiple="true"
          >
            <a-button type="primary" :loading="uploading">上传文件</a-button>
          </a-upload>
          <a-button v-if="selectedRowKeys.length" danger @click="batchDelete">
            批量删除 ({{ selectedRowKeys.length }})
          </a-button>
          <a-button @click="refreshAll">刷新</a-button>
          <a-select
            v-model:value="storageType"
            placeholder="存储类型"
            allow-clear
            style="width: 140px"
            @change="fetchList"
          >
            <a-select-option
              v-for="item in storageConfig.providers || []"
              :key="item.value"
              :value="item.value"
            >
              {{ item.label }}
            </a-select-option>
          </a-select>
          <a-input-search
            v-model:value="searchText"
            placeholder="搜索文件名"
            style="width: 220px"
            @search="fetchList"
          />
        </a-space>
      </a-card>
    </div>

    <div class="table-wrapper">
      <NtestercTableCard title="文件列表">
        <NtestercTable
          row-key="id"
          :columns="columns"
          :data-source="dataSource"
          :loading="tableLoading"
          :row-selection="{ selectedRowKeys, onChange: onSelectChange }"
          :pagination="pagination"
          @change="handleTableChange"
          :scroll="{ x: 1000, y: 'calc(100vh - 560px)' }"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'storage_type'">
              <a-tag>{{ STORAGE_TYPE_LABELS[record.storage_type] || record.storage_type }}</a-tag>
            </template>
            <template v-else-if="column.dataIndex === 'file_size'">
              {{ formatSize(record.file_size) }}
            </template>
            <template v-else-if="column.dataIndex === 'operation'">
              <a @click="downloadFile(record)">下载</a>
              <a-divider type="vertical" />
              <a style="color: #ff4d4f" @click="removeFile(record)">删除</a>
            </template>
          </template>
        </NtestercTable>
      </NtestercTableCard>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { message, Modal } from 'ant-design-vue'
import PageHeader from '@/components/PageHeader.vue'
import NtestercTable from '@/components/ntesterc/NtestercTable.vue'
import NtestercTableCard from '@/components/ntesterc/NtestercTableCard.vue'
import {
  STORAGE_TYPE_LABELS,
  uploadFile,
  getFileList,
  getFileStatistics,
  getStorageConfig,
  deleteFile,
  deleteFileList,
  getFileDownloadUrl,
} from '@/api/file'

const tableLoading = ref(false)
const uploading = ref(false)
const dataSource = ref<any[]>([])
const searchText = ref('')
const storageType = ref<string | undefined>()
const selectedRowKeys = ref<string[]>([])
const statistics = ref<Record<string, number>>({})
const storageConfig = ref<Record<string, any>>({})

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (t: number) => `共 ${t} 条`,
})

const columns = [
  { title: '文件名', dataIndex: 'original_name', ellipsis: true },
  { title: '存储', dataIndex: 'storage_type', width: 120 },
  { title: '类型', dataIndex: 'extend_name', width: 90 },
  { title: '大小', dataIndex: 'file_size', width: 100 },
  { title: '上传者', dataIndex: 'uploader_name', width: 110 },
  { title: '上传时间', dataIndex: 'created_at', width: 170 },
  { title: '操作', dataIndex: 'operation', width: 120, fixed: 'right' },
]

function formatSize (kb: number | string | undefined) {
  const n = Number(kb || 0)
  if (n < 1024) return `${n.toFixed(1)} KB`
  return `${(n / 1024).toFixed(2)} MB`
}

function onSelectChange (keys: string[]) {
  selectedRowKeys.value = keys
}

async function loadMeta () {
  const [statRes, cfgRes] = await Promise.all([getFileStatistics(), getStorageConfig()])
  statistics.value = statRes.data?.data || {}
  storageConfig.value = cfgRes.data?.data || {}
}

async function fetchList () {
  tableLoading.value = true
  try {
    const res = await getFileList({
      page: pagination.current,
      page_size: pagination.pageSize,
      name: searchText.value || undefined,
      storage_type: storageType.value || undefined,
    })
    const body = res.data || {}
    dataSource.value = body.data || []
    pagination.total = body.total || 0
  } finally {
    tableLoading.value = false
  }
}

function handleTableChange (pag: any) {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchList()
}

async function refreshAll () {
  await loadMeta()
  await fetchList()
}

async function handleUpload (options: any) {
  const { file, onSuccess, onError } = options
  const formData = new FormData()
  formData.append('file', file as File)
  uploading.value = true
  try {
    await uploadFile(formData)
    message.success('上传成功')
    onSuccess?.({})
    await refreshAll()
  } catch (e) {
    onError?.(e)
  } finally {
    uploading.value = false
  }
}

function downloadFile (record: { id: string }) {
  window.open(getFileDownloadUrl(record.id), '_blank')
}

function removeFile (record: { id: string; original_name?: string }) {
  Modal.confirm({
    title: '确认删除',
    content: `确定删除「${record.original_name || record.id}」吗？`,
    onOk: async () => {
      await deleteFile({ id: record.id })
      message.success('已删除')
      await refreshAll()
    },
  })
}

function batchDelete () {
  Modal.confirm({
    title: '批量删除',
    content: `确定删除选中的 ${selectedRowKeys.value.length} 个文件吗？`,
    onOk: async () => {
      await deleteFileList({ ids: selectedRowKeys.value })
      selectedRowKeys.value = []
      message.success('删除完成')
      await refreshAll()
    },
  })
}

onMounted(() => {
  refreshAll()
})
</script>
