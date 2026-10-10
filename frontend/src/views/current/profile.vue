<template>
  <div class="profile-page">
    <page-header />

    <div class="profile-page__hero">
      <div class="profile-page__identity">
        <a-avatar :src="infoForm.avatar" :size="80" class="profile-page__avatar">
          {{ avatarFallback }}
        </a-avatar>
        <div class="profile-page__meta">
          <h2 class="profile-page__name">{{ infoForm.name || infoForm.username || '未命名用户' }}</h2>
          <p class="profile-page__sub">
            <span>{{ infoForm.username || '-' }}</span>
            <span class="dot">·</span>
            <span>{{ infoForm.deptName || '未分配部门' }}</span>
          </p>
          <div class="profile-page__tags">
            <a-tag v-for="role in infoForm.roles" :key="`role-${role}`" color="blue">{{ role }}</a-tag>
            <a-tag v-for="pos in infoForm.positions" :key="`pos-${pos}`">{{ pos }}</a-tag>
            <a-tag v-if="!infoForm.roles.length && !infoForm.positions.length">暂无角色/岗位</a-tag>
          </div>
        </div>
      </div>
      <a-upload
        v-model:file-list="avatarFileList"
        name="file"
        action="/api/system/user/current/avatar/upload"
        :show-upload-list="false"
        :headers="uploadHeaders"
        @change="onAvatarChange"
      >
        <a-button :icon="h(UploadOutlined)">更换头像</a-button>
      </a-upload>
    </div>

    <div class="profile-page__panels">
      <a-card class="profile-page__card" :bordered="false">
        <a-tabs v-model:activeKey="activeTab">
          <a-tab-pane key="basic" tab="基本设置">
            <a-form
              class="max-w-[880px]"
              layout="vertical"
              :model="infoForm"
              @finish="onInfoSubmit"
            >
              <a-row :gutter="20">
                <a-col :xs="24" :md="12">
                  <a-form-item label="姓名" name="name" :rules="[{ required: true, message: '请输入姓名' }]">
                    <a-input v-model:value="infoForm.name" placeholder="请输入姓名" allow-clear />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="性别" name="gender" :rules="[{ required: true, message: '请选择性别' }]">
                    <a-select v-model:value="infoForm.gender" placeholder="请选择性别" allow-clear>
                      <a-select-option :value="1">男</a-select-option>
                      <a-select-option :value="2">女</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="联系电话" name="mobile">
                    <a-input v-model:value="infoForm.mobile" placeholder="请输入联系电话" allow-clear />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="邮箱" name="email" :rules="[{ required: true, message: '请输入邮箱' }]">
                    <a-input v-model:value="infoForm.email" placeholder="请输入邮箱" allow-clear />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="用户名">
                    <a-input :value="infoForm.username" disabled />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="所属部门">
                    <a-input :value="infoForm.deptName" disabled />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="当前角色">
                    <a-select :value="infoForm.roles" mode="multiple" disabled />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="所属岗位">
                    <a-select :value="infoForm.positions" mode="multiple" disabled />
                  </a-form-item>
                </a-col>
              </a-row>
              <a-form-item>
                <a-button type="primary" html-type="submit" :loading="infoSaving">保存基本信息</a-button>
              </a-form-item>
            </a-form>
          </a-tab-pane>

          <a-tab-pane key="password" tab="密码设置">
            <a-form
              class="max-w-[420px]"
              layout="vertical"
              :model="passwordForm"
              @finish="onPasswordSubmit"
            >
              <a-form-item
                label="原密码"
                name="oldPassword"
                :rules="[{ required: true, message: '请输入原密码' }]"
              >
                <a-input-password v-model:value="passwordForm.oldPassword" placeholder="请输入原密码" allow-clear />
              </a-form-item>
              <a-form-item
                label="新密码"
                name="newPassword"
                :rules="[{ required: true, message: '请输入新密码' }]"
              >
                <a-input-password v-model:value="passwordForm.newPassword" placeholder="请输入新密码" allow-clear />
              </a-form-item>
              <a-form-item
                label="确认密码"
                name="repeatPassword"
                :rules="[
                  { required: true, message: '请再次输入密码' },
                  { validator: validateRepeatPassword },
                ]"
              >
                <a-input-password
                  v-model:value="passwordForm.repeatPassword"
                  placeholder="请再次输入新密码"
                  allow-clear
                />
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit" :loading="passwordSaving">修改密码</a-button>
              </a-form-item>
            </a-form>
          </a-tab-pane>
        </a-tabs>
      </a-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, h, onActivated, onMounted, reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import type { UploadChangeParam, UploadProps } from 'ant-design-vue'
import { UploadOutlined } from '@ant-design/icons-vue'
import storage from 'store'
import md5 from 'md5'
import PageHeader from '@/components/PageHeader.vue'
import store from '@/store'
import { updateCurrentUserInfo, changeCurrentUserPassword } from '@/api/system/user'

defineOptions({ name: 'Profile' })

interface ProfileForm {
  name: string
  gender?: number
  mobile: string
  email: string
  username: string
  deptName: string
  positions: string[]
  roles: string[]
  avatar: string
}

interface PasswordForm {
  oldPassword: string
  newPassword: string
  repeatPassword: string
}

const activeTab = ref('basic')
const infoSaving = ref(false)
const passwordSaving = ref(false)
const avatarFileList = ref<UploadProps['fileList']>([])

const infoForm = reactive<ProfileForm>({
  name: '',
  gender: undefined,
  mobile: '',
  email: '',
  username: '',
  deptName: '',
  positions: [],
  roles: [],
  avatar: '',
})

const passwordForm = reactive<PasswordForm>({
  oldPassword: '',
  newPassword: '',
  repeatPassword: '',
})

const token = storage.get('Access-Token') as string | undefined
const uploadHeaders = token ? { Authorization: `Bearer ${token}` } : {}

const avatarFallback = computed(() => {
  const text = infoForm.name || infoForm.username || 'U'
  return text.charAt(0).toUpperCase()
})

function resolveFileUrl(path: string) {
  if (!path) return path
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  return path.startsWith('/') ? path : `/${path}`
}

function loadProfile() {
  const basicInfo = store.state.user.basicInfo || {}
  infoForm.name = String(basicInfo.name || '')
  infoForm.gender = typeof basicInfo.gender === 'number' ? basicInfo.gender : undefined
  infoForm.mobile = String(basicInfo.mobile || '')
  infoForm.email = String(basicInfo.email || '')
  infoForm.username = String(basicInfo.username || '')
  infoForm.deptName = String(basicInfo.dept_name || '')
  infoForm.positions = (basicInfo.positions || [])
    .map((item: { name?: string }) => item.name)
    .filter((name): name is string => Boolean(name))
  infoForm.roles = (basicInfo.roles || [])
    .map((item: { name?: string }) => item.name)
    .filter((name): name is string => Boolean(name))
  infoForm.avatar = resolveFileUrl(String(basicInfo.avatar || ''))
}

function resetPasswordForm() {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.repeatPassword = ''
}

async function onInfoSubmit() {
  infoSaving.value = true
  try {
    const response = await updateCurrentUserInfo({
      name: infoForm.name,
      gender: infoForm.gender,
      mobile: infoForm.mobile,
      email: infoForm.email,
      avatar: infoForm.avatar,
    })
    message.success(response.data.message || '更新成功')
    await store.dispatch('getUserInfo')
    loadProfile()
  } catch (error) {
    console.log(error)
  } finally {
    infoSaving.value = false
  }
}

const validateRepeatPassword: Rule['validator'] = async (_rule, value) => {
  if (value && value !== passwordForm.newPassword) {
    return Promise.reject('两次密码输入不一致')
  }
  return Promise.resolve()
}

async function onPasswordSubmit() {
  if (passwordForm.newPassword !== passwordForm.repeatPassword) {
    message.error('两次密码输入不一致')
    return
  }
  passwordSaving.value = true
  try {
    const response = await changeCurrentUserPassword({
      old_password: md5(passwordForm.oldPassword),
      new_password: md5(passwordForm.newPassword),
    })
    message.success(response.data.message || '修改成功')
    resetPasswordForm()
  } catch (error) {
    console.log(error)
  } finally {
    passwordSaving.value = false
  }
}

function onAvatarChange(info: UploadChangeParam) {
  if (info.file.status === 'done') {
    const response = info.file.response as { code?: number; data?: string; message?: string }
    const path = response?.data
    if (!path || response?.code !== 200) {
      message.error(response?.message || '上传失败')
      return
    }
    const nextAvatar = resolveFileUrl(path)
    infoForm.avatar = nextAvatar
    store.commit('setAvatar', nextAvatar)
    message.success('上传成功')
  } else if (info.file.status === 'error') {
    message.error('上传失败')
  }
}

onMounted(loadProfile)
onActivated(loadProfile)
</script>

<style lang="scss" scoped>
.profile-page {
  &__hero {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    justify-content: space-between;
    min-height: 128px;
    margin-bottom: 16px;
    padding: 28px 32px;
    background: var(--ntesterc-card-bg);
    border: 1px solid var(--ntesterc-border);
    border-radius: 12px;
    box-shadow: var(--ntesterc-shadow);
  }

  &__identity {
    display: flex;
    gap: 20px;
    align-items: center;
    min-width: 0;
  }

  &__avatar {
    flex-shrink: 0;
    background: var(--ntesterc-primary);
    color: #fff;
  }

  &__meta {
    min-width: 0;
  }

  &__name {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    line-height: 1.35;
    color: var(--ntesterc-text);
  }

  &__sub {
    margin: 8px 0 12px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--ntesterc-text-secondary);

    .dot {
      margin: 0 6px;
    }
  }

  &__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  &__card {
    background: var(--ntesterc-card-bg);
    border: 1px solid var(--ntesterc-border);
    border-radius: 12px;
    box-shadow: var(--ntesterc-shadow);

    :deep(.ant-card-body) {
      padding: 8px 24px 24px;
    }

    :deep(.ant-tabs-nav) {
      margin-bottom: 20px;
    }
  }
}

@media (max-width: 768px) {
  .profile-page__hero {
    align-items: flex-start;
    padding: 24px 20px;
  }
}
</style>
