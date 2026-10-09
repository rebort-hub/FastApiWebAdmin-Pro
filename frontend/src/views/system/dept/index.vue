<template>
  <div class="dept-page">
    <page-header />

    <div class="dept-page__body">
      <aside class="dept-page__sider">
        <a-card class="dept-page__tree-card" :bordered="false">
          <template #title>
            <span class="dept-page__card-title">部门列表</span>
          </template>
          <template #extra>
            <a-space :size="8">
              <a-button type="primary" size="small" :icon="h(PlusOutlined)" @click="openCreateModal">
                新建
              </a-button>
              <a-dropdown>
                <template #overlay>
                  <a-menu @click="handleTreeActions">
                    <a-menu-item key="expand"><ArrowsAltOutlined /> 展开全部</a-menu-item>
                    <a-menu-item key="collapse"><ShrinkOutlined /> 折叠全部</a-menu-item>
                  </a-menu>
                </template>
                <a-button size="small">操作 <DownOutlined /></a-button>
              </a-dropdown>
            </a-space>
          </template>

          <div class="dept-page__tree-toolbar">
            <a-input
              v-model:value="treeKeyword"
              allow-clear
              placeholder="搜索部门"
              :prefix="h(SearchOutlined)"
            />
            <a-switch
              v-model:checked="showAllDept"
              checked-children="全部"
              un-checked-children="启用"
              @change="rebuildTree"
            />
          </div>

          <a-spin :spinning="treeLoading">
            <a-tree
              v-if="!treeLoading"
              v-model:selectedKeys="selectedKeys"
              v-model:expandedKeys="expandedKeys"
              :tree-data="filteredTreeData"
              :field-names="{ children: 'children', title: 'name', key: 'id' }"
              :show-line="{ showLeafIcon: false }"
              block-node
              @select="onDeptSelect"
            >
              <template #title="{ name, available }">
                <span :class="{ 'is-disabled': !available }">{{ name }}</span>
              </template>
            </a-tree>
            <a-empty v-if="!treeLoading && !filteredTreeData.length" :image="Empty.PRESENTED_IMAGE_SIMPLE" />
          </a-spin>
        </a-card>
      </aside>

      <section class="dept-page__main">
        <NtestercTableCard :title="userTableTitle">
          <template #extra>
            <a-space :size="8">
              <a-button
                size="small"
                :disabled="!selectedDept"
                :icon="h(EditOutlined)"
                @click="openEditDrawer"
              >
                编辑部门
              </a-button>
              <a-button
                size="small"
                danger
                :disabled="!selectedDept"
                :icon="h(DeleteOutlined)"
                :loading="deptDeleting"
                @click="confirmDeleteDept"
              >
                删除部门
              </a-button>
            </a-space>
          </template>

          <div class="dept-page__user-search">
            <a-form layout="inline" :model="userQuery" @finish="onUserSearch">
              <a-form-item name="username" label="用户名">
                <a-input
                  v-model:value="userQuery.username"
                  allow-clear
                  placeholder="请输入用户名"
                  style="width: 160px"
                />
              </a-form-item>
              <a-form-item name="name" label="姓名">
                <a-input
                  v-model:value="userQuery.name"
                  allow-clear
                  placeholder="请输入姓名"
                  style="width: 160px"
                />
              </a-form-item>
              <a-form-item name="available" label="状态">
                <a-select
                  v-model:value="userQuery.available"
                  allow-clear
                  placeholder="全部"
                  style="width: 120px"
                >
                  <a-select-option value="true">启用</a-select-option>
                  <a-select-option value="false">停用</a-select-option>
                </a-select>
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit" :loading="tableLoading" :disabled="!selectedDept">
                  查询
                </a-button>
                <a-button style="margin-left: 8px" :disabled="!selectedDept" @click="resetUserQuery">
                  重置
                </a-button>
              </a-form-item>
            </a-form>
          </div>

          <a-empty
            v-if="!selectedDept"
            class="dept-page__empty"
            description="请选择左侧部门查看所属用户"
          />
          <NtestercTable
            v-else
            :row-key="(record: DeptUserRow) => record.id"
            :columns="columns"
            :data-source="userList"
            :loading="tableLoading"
            :pagination="pagination"
            :scroll="{ x: 900, y: 'calc(100vh - 420px)' }"
            @change="handleTableChange"
          >
            <template #bodyCell="{ column, record, index }">
              <template v-if="column.dataIndex === 'index'">
                {{ (pagination.current - 1) * pagination.pageSize + index + 1 }}
              </template>
              <template v-else-if="column.dataIndex === 'roles'">
                {{ record.roleNames || '-' }}
              </template>
              <template v-else-if="column.dataIndex === 'positions'">
                {{ record.positionNames || '-' }}
              </template>
              <template v-else-if="column.dataIndex === 'gender'">
                <a-tag :color="record.gender === 1 ? 'blue' : 'pink'">
                  {{ record.gender === 1 ? '男' : '女' }}
                </a-tag>
              </template>
              <template v-else-if="column.dataIndex === 'available'">
                <a-badge :color="record.available ? 'green' : 'red'" />
                {{ record.available ? '启用' : '停用' }}
              </template>
            </template>
          </NtestercTable>
        </NtestercTableCard>
      </section>
    </div>

    <a-modal
      v-model:open="createOpen"
      title="新建部门"
      wrap-class-name="ntesterc-form-modal"
      :width="520"
      :destroy-on-close="true"
      :confirm-loading="createLoading"
      @ok="submitCreate"
    >
      <a-form ref="createFormRef" layout="vertical" :model="createState">
        <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
          <a-input v-model:value="createState.name" placeholder="请输入名称" allow-clear />
        </a-form-item>
        <a-form-item name="order" label="排序">
          <a-input-number v-model:value="createState.order" :min="1" style="width: 100%" />
        </a-form-item>
        <a-form-item name="parent_id" label="上级部门">
          <a-tree-select
            v-model:value="createState.parent_id"
            :tree-data="deptTreeData"
            :field-names="{ children: 'children', label: 'name', value: 'id' }"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            tree-node-filter-prop="name"
            placeholder="不选则为顶级部门"
            allow-clear
            show-search
            style="width: 100%"
          />
        </a-form-item>
        <a-form-item name="description" label="备注">
          <a-textarea v-model:value="createState.description" :rows="4" placeholder="请输入备注" allow-clear />
        </a-form-item>
      </a-form>
    </a-modal>

    <a-drawer
      v-model:open="editOpen"
      class="ntesterc-form-drawer"
      title="编辑部门"
      placement="right"
      :width="480"
      :destroy-on-close="true"
    >
      <template #footer>
        <a-space>
          <a-button @click="editOpen = false">取消</a-button>
          <a-button type="primary" :loading="editLoading" @click="submitEdit">保存</a-button>
        </a-space>
      </template>
      <a-form ref="editFormRef" layout="vertical" :model="editState">
        <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
          <a-input v-model:value="editState.name" placeholder="请输入名称" allow-clear />
        </a-form-item>
        <a-form-item name="order" label="排序">
          <a-input-number v-model:value="editState.order" :min="1" style="width: 100%" />
        </a-form-item>
        <a-form-item name="parent_id" label="上级部门">
          <a-tree-select
            v-model:value="editState.parent_id"
            :tree-data="deptTreeData"
            :field-names="{ children: 'children', label: 'name', value: 'id' }"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            tree-node-filter-prop="name"
            placeholder="不选则为顶级部门"
            allow-clear
            show-search
            style="width: 100%"
          />
        </a-form-item>
        <a-form-item name="available" label="状态">
          <a-radio-group v-model:value="editState.available">
            <a-radio :value="true">启用</a-radio>
            <a-radio :value="false">停用</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item name="description" label="备注">
          <a-textarea v-model:value="editState.description" :rows="4" placeholder="请输入备注" allow-clear />
        </a-form-item>
      </a-form>
    </a-drawer>
  </div>
</template>

<script lang="ts" setup>
import { computed, h, onMounted, reactive, ref } from 'vue'
import { Empty, message, Modal } from 'ant-design-vue'
import type { MenuProps, TableColumnsType, TableProps } from 'ant-design-vue'
import {
  ArrowsAltOutlined,
  DeleteOutlined,
  DownOutlined,
  EditOutlined,
  PlusOutlined,
  SearchOutlined,
  ShrinkOutlined,
} from '@ant-design/icons-vue'
import PageHeader from '@/components/PageHeader.vue'
import NtestercTable from '@/components/ntesterc/NtestercTable.vue'
import NtestercTableCard from '@/components/ntesterc/NtestercTableCard.vue'
import { getDeptList, getDeptUsers, createDept, updateDept, deleteDept } from '@/api/dept'
import { cloneDeep, isEmpty, listToTree } from '@/utils/util'
import type { treeDataType } from './types'

defineOptions({ name: 'SystemDept' })

interface DeptUserRow {
  id?: number
  username?: string
  name?: string
  email?: string
  mobile?: string
  gender?: number
  available?: boolean
  roleNames?: string
  positionNames?: string
  roles?: { name?: string }[]
  positions?: { name?: string }[]
  description?: string
}

const treeLoading = ref(false)
const tableLoading = ref(false)
const deptDeleting = ref(false)
const createOpen = ref(false)
const createLoading = ref(false)
const editOpen = ref(false)
const editLoading = ref(false)
const showAllDept = ref(false)
const treeKeyword = ref('')
const selectedKeys = ref<number[]>([])
const expandedKeys = ref<number[]>([])
const deptTreeData = ref<treeDataType[]>([])
const selectedDept = ref<treeDataType | null>(null)
const userList = ref<DeptUserRow[]>([])
const createFormRef = ref()
const editFormRef = ref()

let flatDeptList: treeDataType[] = []

const userQuery = reactive({
  username: '',
  name: '',
  available: 'true' as string | undefined,
})

const pagination = reactive({
  current: 1,
  pageSize: 10,
  showSizeChanger: true,
  total: 0,
  showTotal: (total: number, range: [number, number]) =>
    `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`,
})

const createState = reactive<treeDataType>({
  name: '',
  order: 1,
  parent_id: undefined,
  description: '',
})

const editState = reactive<treeDataType>({
  id: undefined,
  name: '',
  order: 1,
  parent_id: undefined,
  available: true,
  description: '',
})

const columns: TableColumnsType = [
  { title: '序号', dataIndex: 'index', width: 70 },
  { title: '用户名', dataIndex: 'username', width: 120 },
  { title: '姓名', dataIndex: 'name', width: 100 },
  { title: '角色', dataIndex: 'roles', ellipsis: true, width: 140 },
  { title: '岗位', dataIndex: 'positions', ellipsis: true, width: 120 },
  { title: '邮箱', dataIndex: 'email', ellipsis: true, width: 160 },
  { title: '联系电话', dataIndex: 'mobile', width: 120 },
  { title: '性别', dataIndex: 'gender', width: 80 },
  { title: '状态', dataIndex: 'available', width: 90 },
  { title: '备注', dataIndex: 'description', ellipsis: true },
]

const userTableTitle = computed(() =>
  selectedDept.value?.name ? `${selectedDept.value.name} · 所属用户` : '所属用户',
)

function filterTree(nodes: treeDataType[], keyword: string): treeDataType[] {
  if (!keyword) return nodes
  const kw = keyword.trim().toLowerCase()
  const walk = (list: treeDataType[]): treeDataType[] => {
    const result: treeDataType[] = []
    for (const node of list) {
      const children = node.children ? walk(node.children) : []
      if ((node.name || '').toLowerCase().includes(kw) || children.length) {
        result.push({ ...node, children })
      }
    }
    return result
  }
  return walk(nodes)
}

const filteredTreeData = computed(() => filterTree(deptTreeData.value, treeKeyword.value))

function rebuildTree() {
  const source = showAllDept.value ? flatDeptList : flatDeptList.filter((item) => item.available)
  deptTreeData.value = listToTree(cloneDeep(source))
  expandedKeys.value = source.map((item) => item.id!).filter(Boolean)
}

async function loadDeptTree() {
  treeLoading.value = true
  try {
    const response = await getDeptList()
    flatDeptList = response.data.data || []
    rebuildTree()
    if (!selectedKeys.value.length && deptTreeData.value.length) {
      const first = deptTreeData.value[0]
      selectedKeys.value = [first.id!]
      selectedDept.value = cloneDeep(first)
      delete selectedDept.value.children
      await loadUsers()
    } else if (selectedDept.value?.id) {
      const current = flatDeptList.find((item) => item.id === selectedDept.value?.id)
      if (current) {
        selectedDept.value = cloneDeep(current)
        delete selectedDept.value.children
        await loadUsers()
      } else {
        selectedKeys.value = []
        selectedDept.value = null
        userList.value = []
        pagination.total = 0
      }
    }
  } catch (error) {
    console.log(error)
  } finally {
    treeLoading.value = false
  }
}

async function loadUsers() {
  if (!selectedDept.value?.id) {
    userList.value = []
    pagination.total = 0
    return
  }

  tableLoading.value = true
  try {
    const params: Record<string, unknown> = {
      dept_id: selectedDept.value.id,
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (userQuery.username) params.username = userQuery.username
    if (userQuery.name) params.name = userQuery.name
    if (userQuery.available === 'true' || userQuery.available === 'false') {
      params.available = userQuery.available === 'true'
    }

    const response = await getDeptUsers(params)
    const result = response.data
    userList.value = (result.data || []).map((item: DeptUserRow) => ({
      ...item,
      roleNames: item.roles?.map((role) => role.name).filter(Boolean).join('，') || '',
      positionNames: item.positions?.map((pos) => pos.name).filter(Boolean).join('，') || '',
    }))
    pagination.total = result.total || 0
  } catch (error) {
    console.log(error)
  } finally {
    tableLoading.value = false
  }
}

function onDeptSelect(keys: (string | number)[], e: { selectedNodes: treeDataType[] }) {
  if (!keys.length) {
    selectedDept.value = null
    userList.value = []
    pagination.total = 0
    return
  }
  const node = cloneDeep(e.selectedNodes[0])
  delete node.children
  selectedDept.value = node
  pagination.current = 1
  loadUsers()
}

function onUserSearch() {
  pagination.current = 1
  loadUsers()
}

function resetUserQuery() {
  userQuery.username = ''
  userQuery.name = ''
  userQuery.available = 'true'
  pagination.current = 1
  loadUsers()
}

const handleTableChange: TableProps['onChange'] = (pag) => {
  pagination.current = Number(pag?.current || 1)
  pagination.pageSize = Number(pag?.pageSize || 10)
  loadUsers()
}

const handleTreeActions: MenuProps['onClick'] = ({ key }) => {
  if (key === 'expand') {
    expandedKeys.value = flatDeptList.map((item) => item.id!).filter(Boolean)
    return
  }
  expandedKeys.value = []
}

function openCreateModal() {
  createState.name = ''
  createState.order = 1
  createState.parent_id = selectedDept.value?.id
  createState.description = ''
  createOpen.value = true
}

async function submitCreate() {
  createLoading.value = true
  try {
    await createFormRef.value.validate()
    const body = cloneDeep(createState) as Record<string, unknown>
    Object.keys(body).forEach((key) => {
      if (isEmpty(body[key])) delete body[key]
    })
    const response = await createDept(body)
    message.success(response.data.message)
    createOpen.value = false
    await loadDeptTree()
  } catch (error) {
    console.log(error)
  } finally {
    createLoading.value = false
  }
}

function openEditDrawer() {
  if (!selectedDept.value) return
  Object.assign(editState, {
    id: selectedDept.value.id,
    name: selectedDept.value.name,
    order: selectedDept.value.order ?? 1,
    parent_id: selectedDept.value.parent_id,
    available: selectedDept.value.available ?? true,
    description: selectedDept.value.description || '',
  })
  editOpen.value = true
}

async function submitEdit() {
  editLoading.value = true
  try {
    await editFormRef.value.validate()
    const response = await updateDept({ ...editState })
    message.success(response.data.message)
    editOpen.value = false
    await loadDeptTree()
  } catch (error) {
    console.log(error)
  } finally {
    editLoading.value = false
  }
}

function confirmDeleteDept() {
  if (!selectedDept.value?.id) return
  Modal.confirm({
    title: '提示',
    content: `确定删除部门「${selectedDept.value.name}」吗？`,
    async onOk() {
      deptDeleting.value = true
      try {
        const response = await deleteDept({ id: selectedDept.value!.id })
        message.success(response.data.message)
        selectedKeys.value = []
        selectedDept.value = null
        userList.value = []
        pagination.total = 0
        await loadDeptTree()
      } catch (error) {
        console.log(error)
      } finally {
        deptDeleting.value = false
      }
    },
  })
}

onMounted(() => {
  loadDeptTree()
})
</script>

<style lang="scss" scoped>
.dept-page {
  &__body {
    display: flex;
    gap: 16px;
    align-items: stretch;
    min-height: calc(100vh - 180px);
  }

  &__sider {
    flex: 0 0 300px;
    width: 300px;
    min-width: 260px;
  }

  &__main {
    flex: 1;
    min-width: 0;
  }

  &__tree-card {
    height: 100%;
    background: var(--ntesterc-card-bg);
    border: 1px solid var(--ntesterc-border);
    border-radius: 12px;
    box-shadow: var(--ntesterc-shadow);

    :deep(.ant-card-head) {
      min-height: 56px;
      padding: 0 16px;
      border-bottom: 1px solid var(--ntesterc-border);
    }

    :deep(.ant-card-body) {
      padding: 12px 12px 16px;
      max-height: calc(100vh - 220px);
      overflow: auto;
    }
  }

  &__card-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--ntesterc-text);
  }

  &__tree-toolbar {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 12px;
  }

  &__user-search {
    margin-bottom: 12px;
  }

  &__empty {
    margin: 80px 0;
  }

  :deep(.ant-tree) {
    background: transparent;
  }

  :deep(.ant-tree-node-selected) {
    background: var(--ntesterc-menu-active) !important;
  }

  :deep(.is-disabled) {
    color: #ff4d4f;
  }
}

@media (max-width: 992px) {
  .dept-page__body {
    flex-direction: column;
  }

  .dept-page__sider {
    flex: none;
    width: 100%;
  }
}
</style>
