<template>
  <div>
    <page-header />
    <div class="table-wrapper">
      <NtestercTableCard title="菜单列表">
        <template #extra>
          <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"  style="margin-right: 10px;">新建</a-button>
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleMoreClick">
                <a-menu-item key="1"><span style="margin-right: 10px;"><CheckOutlined /></span><span>批量启用</span></a-menu-item>
                <a-menu-item key="2"><span style="margin-right: 10px;"><StopOutlined /></span><span>批量停用</span></a-menu-item>
              </a-menu>
            </template>
            <a-button>更多<DownOutlined />
            </a-button>
          </a-dropdown>
        </template>
        <NtestercTable :rowKey="record => record.id" :columns="columns" :data-source="menuTreeData" :row-selection="rowSelection" :loading="tableLoading" 
          :scroll="{ x: 500, y: 'calc(100vh - 350px)' }" :pagination="false" :style="{ minHeight: '700px' }">
          <template v-slot:bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'icon'">
              <span v-if="record.icon && resolveIcon(record.icon)" class="menu-icon-cell">
                <component :is="resolveIcon(record.icon)" />
              </span>
              <span v-else class="menu-icon-cell is-empty">-</span>
            </template>
            <template v-else-if="column.dataIndex === 'type'">
              <a-tag :color="record.type === 1 ? 'blue' : (record.type === 2 ? 'green' : 'orange')">
                {{ record.type === 1 ? '目录' : (record.type === 2 ? '功能' : '权限') }}
              </a-tag>
            </template>
            <template v-else-if="column.dataIndex === 'available'">
              <span>
                <a-badge :color="record.available ? 'green' : 'red'" />
                {{ record.available ? '启用' : '禁用' }}
              </span>
            </template>
            <template v-else-if="column.dataIndex === 'operation'">
              <div class="ntesterc-table__actions">
                <a @click="modalHandle('view', record)">查看</a>
                <a @click="modalHandle('update', record)">修改</a>
                <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消" @confirm="deleteRow(record)">
                  <a>删除</a>
                </a-popconfirm>
              </div>
            </template>
          </template>
        </NtestercTable>
      </NtestercTableCard>
    </div>

    <div>
      <a-drawer
        v-model:open="openModal"
        class="ntesterc-form-drawer"
        placement="right"
        :width="modalTitle === 'view' ? 720 : 560"
        :destroy-on-close="true"
        :title="modalTitle === 'create' ? '新建菜单' : modalTitle === 'view' ? '查看菜单' : '修改菜单'"
      >
        <template #footer>
          <a-button v-if="modalTitle === 'view'" @click="openModal = false">关闭</a-button>
          <a-space v-else>
            <a-button @click="openModal = false">取消</a-button>
            <a-button type="primary" :loading="modalSubmitLoading" @click="handleModalSumbit">确定</a-button>
          </a-space>
        </template>
        <div v-if="modalTitle === 'view'">
          <a-spin :spinning="detailStateLoading">
            <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }" bordered>
              <a-descriptions-item label="菜单名称">{{ detailState.name }}</a-descriptions-item>
              <a-descriptions-item label="菜单类型">
                <a-tag :color="detailState.type === 1 ? 'blue' : (detailState.type === 2 ? 'green' : 'orange')">
                  {{ detailState.type === 1 ? '目录' : (detailState.type === 2 ? '功能' : '权限') }}
                </a-tag>
              </a-descriptions-item>
              <a-descriptions-item label="显示排序">{{ detailState.order }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="图标">
                <span v-if="detailState.icon && resolveIcon(detailState.icon)" class="menu-icon-detail">
                  <component :is="resolveIcon(detailState.icon)" />
                  <span>{{ detailState.icon }}</span>
                </span>
                <span v-else>-</span>
              </a-descriptions-item>
              <a-descriptions-item label="父级菜单" :span="2">{{ detailState.parent_name }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 1" label="权限标识" :span="2">{{ detailState.permission }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="路由名称">{{ detailState.route_name }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="路由路径">{{ detailState.route_path }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type === 1" label="重定向">{{ detailState.redirect }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type === 2" label="组件地址">{{ detailState.component_path }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="是否缓存">{{ detailState.cache ? '是': '否' }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="是否隐藏">{{ detailState.hidden ? '是': '否' }}</a-descriptions-item>
              <a-descriptions-item label="状态">
                <a-badge :color="detailState.available ? 'green' : 'red'" />{{ detailState.available ? '启用' : '禁用' }}
              </a-descriptions-item>
              <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
              <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
              <a-descriptions-item label="备注" :span="2">{{ detailState.description }}</a-descriptions-item>
            </a-descriptions>
          </a-spin>
        </div>
        <div v-else-if="modalTitle === 'create'">
          <a-form ref="createForm" layout="vertical" :model="createState">
            <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
              <a-input v-model:value="createState.name" placeholder="请输入名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="type" label="类型" :rules="[{ required: true, message: '请选择类型' }]">
              <a-radio-group v-model:value="createState.type">
                <a-radio :value="1">目录</a-radio>
                <a-radio :value="2">功能</a-radio>
                <a-radio :value="3">权限</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item
              v-if="createState.type !== 1"
              name="permission"
              label="权限标识"
              :rules="[{ required: createState.type !== 1 ? true : false, message: '请输入权限标识' }]"
            >
              <a-input v-model:value="createState.permission" placeholder="请输入权限标识" allowClear></a-input>
            </a-form-item>
            <a-form-item name="parent_id" label="父级菜单">
              <a-tree-select
                v-model:value="createState.parent_id"
                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                :tree-data="menuSelectorTreeData"
                :field-names="{ children: 'children', label: 'name', value: 'id' }"
                tree-node-filter-prop="name"
                style="width: 100%"
                show-search
                allow-clear
              ></a-tree-select>
            </a-form-item>
            <a-form-item name="icon" label="图标">
              <a-popover
                v-model:open="iconPopoverOpen"
                placement="bottomLeft"
                trigger="click"
                overlay-class-name="menu-icon-popover"
              >
                <template #content>
                  <div class="icon-picker">
                    <div class="icon-picker__toolbar">
                      <a-form-item-rest>
                        <a-input
                          v-model:value="iconSelector.search"
                          allow-clear
                          placeholder="搜索图标名称"
                          :prefix="h(SearchOutlined)"
                        />
                      </a-form-item-rest>
                      <a-button type="link" danger :disabled="!createState.icon" @click="iconClearClickHandle">
                        清空
                      </a-button>
                    </div>
                    <a-tabs
                      v-model:activeKey="iconSelector.activeTab"
                      size="small"
                      class="icon-picker__tabs"
                      @change="iconTabHandleChange"
                    >
                      <a-tab-pane v-for="(group, index) in iconDataSource" :key="index" :tab="group.type" />
                    </a-tabs>
                    <div class="icon-picker__grid">
                      <a-tooltip
                        v-for="item in pagedIcons"
                        :key="item.name"
                        :title="item.name"
                      >
                        <button
                          type="button"
                          class="icon-picker__item"
                          :class="{ 'is-active': createState.icon === item.name }"
                          @click="iconHandleClick(item)"
                        >
                          <component :is="item.icon" />
                        </button>
                      </a-tooltip>
                    </div>
                    <div class="icon-picker__footer">
                      <a-pagination
                        size="small"
                        :current="pagination.current"
                        :page-size="pagination.pageSize"
                        :total="pagination.total"
                        :show-size-changer="false"
                        :show-quick-jumper="false"
                        :show-less-items="true"
                        :show-total="iconPaginationTotal"
                        @change="onIconPaginationChange"
                      />
                    </div>
                  </div>
                </template>
                <a-button class="icon-picker__trigger">
                  <template v-if="createIconComp" #icon>
                    <component :is="createIconComp" />
                  </template>
                  <span :class="{ 'icon-picker__placeholder': !createState.icon }">
                    {{ createState.icon || '请选择图标' }}
                  </span>
                </a-button>
              </a-popover>
            </a-form-item>
            <a-form-item name="order" label="排序">
              <a-input-number v-model:value="createState.order" :min="1" />
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
            <div v-if="createState.type !== 3">
              <a-form-item name="route_name" label="路由名称" :rules="[{ required: createState.type !== 3 ? true : false, message: '请输入路由名称' }]">
                <a-input v-model:value="createState.route_name" placeholder="请输入路由名称" allowClear></a-input>
              </a-form-item>
              <a-form-item name="route_path" label="路由路径" :rules="[{ required: createState.type !== 3 ? true : false, message: '请输入路由路径' }]">
                <a-input v-model:value="createState.route_path" placeholder="请输入路由路径" allowClear></a-input>
              </a-form-item>
              <a-form-item  v-if="createState.type === 1" name="redirect" label="重定向" :rules="[{ required: createState.type === 1 ? true : false, message: '请输入重定向' }]">
                <a-input v-model:value="createState.redirect" placeholder="请输入重定向" allowClear></a-input>
              </a-form-item>
              <a-form-item v-if="createState.type === 2" name="component_path" label="组件地址" :rules="[{ required: createState.type === 2 ? true : false, message: '请输入组件地址' }]">
                <a-input v-model:value="createState.component_path" placeholder="请输入组件地址" allowClear></a-input>
              </a-form-item>
              <a-form-item name="cache" label="是否缓存" :rules="[{ required: createState.type !== 3 ? true : false, message: '请选择缓存状态' }]">
                <a-switch v-model:checked="createState.cache"></a-switch>
              </a-form-item>
              <a-form-item name="hidden" label="是否隐藏" :rules="[{ required: createState.type !== 3 ? true : false, message: '请选择隐藏状态' }]">
                <a-switch v-model:checked="createState.hidden"></a-switch>
              </a-form-item>
            </div>
          </a-form>
        </div>
        <div v-else>
          <a-form ref="updateForm" layout="vertical" :model="updateState">
            <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
              <a-input v-model:value="updateState.name" placeholder="请输入名称" allowClear></a-input>
            </a-form-item>
            <a-form-item
              v-if="updateState.type !== 1"
              name="permission"
              label="权限标识"
              :rules="[{ required: updateState.type !== 1 ? true : false, message: '请输入权限标识' }]"
            >
              <a-input v-model:value="updateState.permission" placeholder="请输入权限标识" allowClear></a-input>
            </a-form-item>
            <a-form-item name="parent_id" label="父级菜单">
              <a-tree-select
                v-model:value="updateState.parent_id"
                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                :tree-data="menuSelectorTreeData"
                :field-names="{ children: 'children', label: 'name', value: 'id' }"
                tree-node-filter-prop="name"
                style="width: 100%"
                show-search
                allow-clear
              ></a-tree-select>
            </a-form-item>
            <a-form-item name="icon" label="图标">
              <a-popover
                v-model:open="iconPopoverOpen"
                placement="bottomLeft"
                trigger="click"
                overlay-class-name="menu-icon-popover"
              >
                <template #content>
                  <div class="icon-picker">
                    <div class="icon-picker__toolbar">
                      <a-form-item-rest>
                        <a-input
                          v-model:value="iconSelector.search"
                          allow-clear
                          placeholder="搜索图标名称"
                          :prefix="h(SearchOutlined)"
                        />
                      </a-form-item-rest>
                      <a-button type="link" danger :disabled="!updateState.icon" @click="iconClearClickHandle">
                        清空
                      </a-button>
                    </div>
                    <a-tabs
                      v-model:activeKey="iconSelector.activeTab"
                      size="small"
                      class="icon-picker__tabs"
                      @change="iconTabHandleChange"
                    >
                      <a-tab-pane v-for="(group, index) in iconDataSource" :key="index" :tab="group.type" />
                    </a-tabs>
                    <div class="icon-picker__grid">
                      <a-tooltip
                        v-for="item in pagedIcons"
                        :key="item.name"
                        :title="item.name"
                      >
                        <button
                          type="button"
                          class="icon-picker__item"
                          :class="{ 'is-active': updateState.icon === item.name }"
                          @click="iconHandleClick(item)"
                        >
                          <component :is="item.icon" />
                        </button>
                      </a-tooltip>
                    </div>
                    <div class="icon-picker__footer">
                      <a-pagination
                        size="small"
                        :current="pagination.current"
                        :page-size="pagination.pageSize"
                        :total="pagination.total"
                        :show-size-changer="false"
                        :show-quick-jumper="false"
                        :show-less-items="true"
                        :show-total="iconPaginationTotal"
                        @change="onIconPaginationChange"
                      />
                    </div>
                  </div>
                </template>
                <a-button class="icon-picker__trigger">
                  <template v-if="updateIconComp" #icon>
                    <component :is="updateIconComp" />
                  </template>
                  <span :class="{ 'icon-picker__placeholder': !updateState.icon }">
                    {{ updateState.icon || '请选择图标' }}
                  </span>
                </a-button>
              </a-popover>
            </a-form-item>
            <a-form-item name="order" label="排序">
              <a-input-number v-model:value="updateState.order" :min="1" />
            </a-form-item>
            <a-form-item name="available" label="状态">
              <a-radio-group v-model:value="updateState.available">
                <a-radio :value="true">启用</a-radio>
                <a-radio :value="false">停用</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="updateState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
            <div v-if="updateState.type !== 3">
              <a-form-item name="route_name" label="路由名称" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请输入路由名称' }]">
                <a-input v-model:value="updateState.route_name" placeholder="请输入路由名称" allowClear></a-input>
              </a-form-item>
              <a-form-item name="route_path" label="路由路径" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请输入路由路径' }]">
                <a-input v-model:value="updateState.route_path" placeholder="请输入路由路径" allowClear></a-input>
              </a-form-item>
              <a-form-item v-if="updateState.type === 1" name="redirect" label="重定向" :rules="[{ required: updateState.type === 1 ? true : false, message: '请输入重定向' }]">
                <a-input v-model:value="updateState.redirect" placeholder="请输入重定向" allowClear></a-input>
              </a-form-item>
              <a-form-item v-if="updateState.type === 2" name="component_path" label="组件地址" :rules="[{ required: updateState.type === 2 ? true : false, message: '请输入组件地址' }]">
                <a-input v-model:value="updateState.component_path" placeholder="请输入组件地址" allowClear></a-input>
              </a-form-item>
              <a-form-item name="cache" label="是否缓存" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请选择缓存状态' }]">
                <a-switch v-model:checked="updateState.cache"></a-switch>
              </a-form-item>
              <a-form-item name="hidden" label="是否隐藏" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请选择隐藏状态' }]">
                <a-switch v-model:checked="updateState.hidden"></a-switch>
              </a-form-item>
            </div>
          </a-form>
        </div>
      </a-drawer>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, h, onMounted, watch } from 'vue';
import PageHeader from '@/components/PageHeader.vue';
import NtestercTable from '@/components/ntesterc/NtestercTable.vue';
import NtestercTableCard from '@/components/ntesterc/NtestercTableCard.vue';
import { message, Modal } from 'ant-design-vue';
import { getMenuList, createMenu, updateMenu, deleteMenu, batchEnableMenu, batchDisableMenu } from '@/api/system/menu'
import { listToTree, cloneDeep, isEmpty } from '@/utils/util';
import type { TableColumnsType, MenuProps } from 'ant-design-vue';
import * as AntdIcons from '@ant-design/icons-vue';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined, SearchOutlined } from '@ant-design/icons-vue';
import type { Component } from 'vue'
import type { tableDataType } from './types'
import axios from "axios"

type IconOption = { name: string; icon: Component }
type IconGroup = { type: string; icons: IconOption[] }

const iconMap = AntdIcons as unknown as Record<string, Component>

function resolveIcon(name?: string | null): Component | null {
  if (!name) return null
  const comp = iconMap[name]
  return typeof comp === 'object' || typeof comp === 'function' ? comp : null
}

const columns: TableColumnsType = [
  {
    title: '菜单名称',
    dataIndex: 'name',
  },
  {
    title: '图标',
    dataIndex: 'icon',
    width: 80,
    align: 'center',
  },
  {
    title: '显示排序',
    dataIndex: 'order',
  },
  {
    title: '菜单类型',
    dataIndex: 'type',
  },
  {
    title: '权限标识',
    dataIndex: 'permission',
  },
  {
    title: '状态',
    dataIndex: 'available',
  },
  {
    title: '备注',
    dataIndex: 'description',
    ellipsis: true,
    width: 200
  },
  {
    title: '操作',
    dataIndex: 'operation',
    fixed: 'right',
    width: 150
  }
];

const menuTreeData = ref<tableDataType[]>([]);
const menuSelectorTreeData = ref<tableDataType[]>([])
const tableLoading = ref(false);
const detailStateLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const createForm = ref();
const updateForm = ref();
const iconSelector = ref<{ activeTab: number; search?: string }>({ activeTab: 0, search: undefined })
const iconPopoverOpen = ref(false)
const iconDataSource = ref<IconGroup[]>([])
const iconData = ref<IconOption[]>([])

const createState: tableDataType = reactive({
  name: '',
  type: 1,
  icon: '',
  order: 1,
  permission: '',
  route_name: '',
  route_path: '',
  component_path: '',
  redirect: '',
  parent_id: undefined,
  cache: true,
  hidden: false,
  description: ''
})
const updateState: tableDataType = reactive({
  id: undefined,
  name: '',
  type: 1,
  icon: '',
  order: 1,
  permission: '',
  route_name: '',
  route_path: '',
  component_path: '',
  redirect: '',
  parent_id: undefined,
  cache: true,
  hidden: false,
  available: true,
  description: ''
})
const detailState = ref<tableDataType>({});

const pagination = reactive({
  current: 1,
  pageSize: 120,
  total: 0,
})

const iconPaginationTotal = (total: number) => `共 ${total}`

const pagedIcons = computed(() => {
  const start = (pagination.current - 1) * pagination.pageSize
  return iconData.value.slice(start, start + pagination.pageSize)
})

const createIconComp = computed(() => resolveIcon(createState.icon))
const updateIconComp = computed(() => resolveIcon(updateState.icon))

function onIconPaginationChange(page: number, pageSize: number) {
  pagination.current = page
  pagination.pageSize = pageSize
}

const loadingData = () => {
  tableLoading.value = true;

  getMenuList().then(response => {
    const result = response.data;
    menuSelectorTreeData.value = listToTree(result.data.filter((item) => item.type !== 3));
    menuTreeData.value = listToTree(result.data);
    tableLoading.value = false;
  }).catch(error => {
    console.log(error);
    tableLoading.value = false;
  })
}

onMounted(() => {
  loadingData();
  axios.get('/icons.json').then(response => {
    const groups: IconGroup[] = []
    response.data.forEach((item: { type: string; icons: string[] }) => {
      const group: IconGroup = { type: item.type, icons: [] }
      item.icons.forEach((iconName: string) => {
        const iconComp = resolveIcon(iconName)
        if (iconComp) {
          group.icons.push({ name: iconName, icon: iconComp })
        }
      })
      groups.push(group)
    })
    iconDataSource.value = groups
    iconData.value = groups[iconSelector.value.activeTab]?.icons || []
    pagination.total = iconData.value.length
  }).catch(error => {
    console.log(error)
  })
});

const selectedRowKeys = ref<tableDataType['id'][]>([]);

const onSelectChange = (selectingRowKeys: tableDataType['id'][]) => {
  console.log(selectingRowKeys);
  
  selectedRowKeys.value = selectingRowKeys;
}

const rowSelection = computed(() => {
  return {
    selectedRowKeys: unref(selectedRowKeys),
    checkStrictly: false,
    onChange: onSelectChange
  }
});

const modalHandle = (modalType: string, record?: tableDataType) => {
  modalTitle.value = modalType;
  openModal.value = true;

  if (modalType === 'view' && record !== undefined) {
    detailStateLoading.value = true;
    detailState.value = record;
    detailStateLoading.value = false;

  } else if (modalType === 'update' && record !== undefined) {
    Object.keys(updateState).forEach(key => {
      updateState[key] = record[key];
    })
  }
  iconSelector.value = {
    activeTab: 0,
    search: undefined
  }
  iconPopoverOpen.value = false
  iconSearch(undefined)
}

const deleteRow = (row: tableDataType) => {
  deleteMenu({ id: row.id }).then(response => {
    message.success(response.data.message);
    loadingData();

  }).catch(error => {
    console.log(error)
  })
}


const handleMoreClick: MenuProps['onClick'] = e => {
  if (!selectedRowKeys.value || !(selectedRowKeys.value.length > 0) ) {
    message.warning('请先勾选数据');
    return;
  }

  Modal.confirm({
    title: '提示',
    content: e.key == 1 ? '是否确定启用选择项？' : '是否确定停用选择项？',
    onOk() {
      const body = { ids: selectedRowKeys.value };
      const batchApi = e.key == 1 ? batchEnableMenu(body) : batchDisableMenu(body);
      batchApi.then(response => {
        message.success(response.data.message);
        selectedRowKeys.value = [];
        loadingData();
      }).catch(error => {
        console.log(error);
      })
    }
  });
}

const handleModalSumbit = () => {
  modalSubmitLoading.value = true;
  if (modalTitle.value === 'view') {
    modalSubmitLoading.value = false;
    openModal.value = false;

  } else if (modalTitle.value === 'create') {
    createForm.value.validate().then(() => {
      const createBody = cloneDeep(createState);
      Object.keys(createBody).forEach(key => {
        if (isEmpty(createBody[key])) {
          delete createBody[key];
        }
      })

      createMenu(createBody).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        Object.keys(createState).forEach(key => delete createState[key])
        createState.type = 1;
        createState.order = 1;
        createState.cache = true;
        createState.hidden = false;
        message.success(response.data.message);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.log(error)
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.log(error)
    })

  } else {
    updateForm.value.validate().then(() => {
      updateMenu(updateState).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        message.success(response.data.message);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.log(error)
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.log(error)
    })
  }
}

watch(() => createState.type, (newType) => {
  Object.keys(createState).forEach(key => delete createState[key])
  createState.type = newType;
  createState.order = 1;
  createState.cache = true;
  createState.hidden = false;
})

watch(() => iconSelector.value.search, (newSearchField) => iconSearch(newSearchField));

const iconSearch = (field?: string) => {
  const group = iconDataSource.value[iconSelector.value.activeTab]
  let activeIcons = group?.icons || []
  if (field) {
    activeIcons = activeIcons.filter(item => item.name.toLowerCase().includes(field.toLowerCase()))
  }
  iconData.value = activeIcons
  pagination.current = 1
  pagination.total = iconData.value.length
}

const iconTabHandleChange = () => iconSearch(iconSelector.value.search)

const iconHandleClick = (values: IconOption) => {
  if (modalTitle.value === 'create') {
    createState.icon = values.name
  } else if (modalTitle.value === 'update') {
    updateState.icon = values.name
  }
  iconPopoverOpen.value = false
}

const iconClearClickHandle = () => {
  if (modalTitle.value === 'create') {
    createState.icon = ''
  } else if (modalTitle.value === 'update') {
    updateState.icon = ''
  }
}

</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}

.menu-icon-cell {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: var(--ant-color-text, rgba(0, 0, 0, 0.88));

  &.is-empty {
    color: var(--ant-color-text-quaternary, rgba(0, 0, 0, 0.25));
    font-size: 14px;
  }
}

.menu-icon-detail {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
}

.icon-picker__trigger {
  display: inline-flex !important;
  align-items: center;
  min-width: 220px;
  justify-content: flex-start;

  :deep(.anticon) {
    font-size: 16px;
  }

  .icon-picker__placeholder {
    color: var(--ant-color-text-placeholder, rgba(0, 0, 0, 0.25));
  }
}

.menu-icon-cell,
.menu-icon-detail {
  :deep(.anticon) {
    display: inline-flex;
    font-size: 18px;
  }
}
</style>

<style lang="scss">
.menu-icon-popover {
  .ant-popover-inner {
    padding: 12px;
  }

  .ant-popover-inner-content {
    padding: 0;
  }
}

.icon-picker {
  width: 488px;

  &__toolbar {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;

    .ant-input-affix-wrapper,
    .ant-input {
      flex: 1;
    }
  }

  &__tabs {
    margin-bottom: 8px;

    .ant-tabs-nav {
      margin-bottom: 0 !important;
    }

    .ant-tabs-nav::before {
      border-bottom-color: var(--ant-color-border-secondary, #f0f0f0);
    }

    .ant-tabs-tab {
      padding: 8px 12px !important;
    }

    .ant-tabs-content-holder {
      display: none;
    }
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(10, 40px);
    grid-auto-rows: 40px;
    gap: 8px;
    justify-content: start;
    align-content: start;
    min-height: 296px;
    max-height: 296px;
    overflow-x: hidden;
    overflow-y: auto;
  }

  &__item {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    flex: none;
    padding: 0;
    border: 1px solid var(--ant-color-border-secondary, #f0f0f0);
    border-radius: 8px;
    background: var(--ant-color-bg-container, #fff);
    color: var(--ant-color-text, rgba(0, 0, 0, 0.88));
    font-size: 18px;
    line-height: 1;
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s, background 0.2s, box-shadow 0.2s;

    .anticon {
      font-size: 18px;
    }

    &:hover {
      border-color: var(--ant-color-primary, #1677ff);
      color: var(--ant-color-primary, #1677ff);
    }

    &.is-active {
      border-color: var(--ant-color-primary, #1677ff);
      color: var(--ant-color-primary, #1677ff);
      background: var(--ant-color-primary-bg, #e6f4ff);
      box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.12);
    }
  }

  &__footer {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
    overflow: hidden;

    .ant-pagination {
      display: flex;
      flex-wrap: nowrap;
      align-items: center;
      justify-content: flex-end;
      margin: 0;
      white-space: nowrap;
    }

    .ant-pagination-total-text {
      flex-shrink: 0;
      margin-inline-end: 8px;
    }

    .ant-pagination-item,
    .ant-pagination-prev,
    .ant-pagination-next {
      flex-shrink: 0;
    }
  }
}
</style>