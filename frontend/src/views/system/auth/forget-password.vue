<template>
  <div class="login-page-root">
    <div class="login-auth-split">
      <div class="login-auth-split__col login-auth-split__col--illustration">
        <LoginLeftView />
      </div>
      <div class="login-auth-split__col login-auth-split__col--form">
        <div class="login-page-panel">
          <div class="login-page-panel__main">
            <div class="auth-right-wrap">
              <div class="form-intro">
                <h3 class="title">忘记密码</h3>
                <p class="sub-title">通过绑定邮箱验证码重置您的登录密码</p>
              </div>

              <div class="step-indicator">
                <div class="step" :class="{ active: state.step >= 1, completed: state.step > 1 }">
                  <div class="step-number">1</div>
                  <div class="step-label">验证身份</div>
                </div>
                <div class="step-divider" />
                <div class="step" :class="{ active: state.step >= 2 }">
                  <div class="step-number">2</div>
                  <div class="step-label">重置密码</div>
                </div>
              </div>

              <a-form
                v-if="state.step === 1"
                ref="step1Ref"
                :model="state.step1"
                :rules="step1Rules"
                layout="vertical"
                @finish="nextStep"
              >
                <a-form-item label="绑定邮箱" name="account">
                  <a-input
                    v-model:value="state.step1.account"
                    placeholder="请输入账号绑定的邮箱"
                    allow-clear
                  />
                </a-form-item>
                <a-form-item label="邮箱验证码" name="code">
                  <div class="email-code-row">
                    <a-input
                      v-model:value="state.step1.code"
                      :maxlength="4"
                      placeholder="4 位数字验证码"
                      allow-clear
                      class="email-code-input"
                    />
                    <a-button
                      class="email-code-btn"
                      :loading="state.sendingCode"
                      :disabled="state.countdown > 0 || !state.step1.account"
                      @click="sendCode"
                    >
                      {{ state.countdown > 0 ? `${state.countdown}s 后重发` : '获取验证码' }}
                    </a-button>
                  </div>
                </a-form-item>
                <a-form-item>
                  <a-button type="primary" html-type="submit" class="auth-submit-btn" :loading="state.loading">
                    下一步
                  </a-button>
                </a-form-item>
              </a-form>

              <a-form
                v-else
                ref="step2Ref"
                :model="state.step2"
                :rules="step2Rules"
                layout="vertical"
                @finish="resetPassword"
              >
                <a-form-item label="新密码" name="newPassword">
                  <a-input-password
                    v-model:value="state.step2.newPassword"
                    autocomplete="new-password"
                    placeholder="至少 6 位"
                  />
                </a-form-item>
                <a-form-item label="确认新密码" name="confirmPassword">
                  <a-input-password
                    v-model:value="state.step2.confirmPassword"
                    autocomplete="new-password"
                    placeholder="再次输入新密码"
                  />
                </a-form-item>
                <div class="step-actions">
                  <a-button @click="state.step = 1">上一步</a-button>
                  <a-button type="primary" html-type="submit" :loading="state.loading">重置密码</a-button>
                </div>
              </a-form>

              <div class="auth-footer-links">
                <router-link to="/login">返回登录</router-link>
              </div>
            </div>
          </div>
          <footer class="login-page-footer">
            <a
              href="https://github.com/rebort-hub/FastApiWebAdmin-Pro"
              target="_blank"
              rel="noopener noreferrer"
            >
              FastApiWebAdmin-Pro
            </a>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message, notification } from 'ant-design-vue'
import type { FormInstance, Rule } from 'ant-design-vue/es/form'
import md5 from 'md5'
import { sendEmailCode, forgetPassword } from '@/api/system/auth'
import LoginLeftView from './LoginLeftView.vue'

const router = useRouter()
const step1Ref = ref<FormInstance>()
const step2Ref = ref<FormInstance>()

const state = reactive({
  step: 1,
  loading: false,
  sendingCode: false,
  countdown: 0,
  step1: {
    account: '',
    code: '',
  },
  step2: {
    newPassword: '',
    confirmPassword: '',
  },
})

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const step1Rules: Record<string, Rule[]> = {
  account: [
    { required: true, message: '请输入绑定邮箱', trigger: 'blur' },
    {
      validator: async (_rule, value) => {
        if (value && !emailPattern.test(value)) {
          return Promise.reject('邮箱格式不正确')
        }
        return Promise.resolve()
      },
      trigger: 'blur',
    },
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 4, message: '验证码为 4 位', trigger: 'blur' },
  ],
}

const validateConfirm = async (_rule: Rule, value: string) => {
  if (!value) {
    return Promise.reject('请再次输入新密码')
  }
  if (value !== state.step2.newPassword) {
    return Promise.reject('两次输入的密码不一致')
  }
  return Promise.resolve()
}

const step2Rules: Record<string, Rule[]> = {
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [{ required: true, validator: validateConfirm, trigger: 'blur' }],
}

const startCountdown = () => {
  state.countdown = 60
  const timer = setInterval(() => {
    state.countdown -= 1
    if (state.countdown <= 0) clearInterval(timer)
  }, 1000)
}

const sendCode = async () => {
  if (!state.step1.account) {
    message.warning('请先输入绑定邮箱')
    return
  }
  if (!emailPattern.test(state.step1.account)) {
    message.warning('邮箱格式不正确')
    return
  }
  state.sendingCode = true
  try {
    const response = await sendEmailCode({
      email: state.step1.account,
    })
    if (response.data?.code === 200) {
      message.success('验证码已发送至绑定邮箱')
      startCountdown()
    }
  } catch {
    /* axios 拦截器已提示 */
  } finally {
    state.sendingCode = false
  }
}

const nextStep = async () => {
  state.step = 2
}

const resetPassword = async () => {
  state.loading = true
  try {
    const response = await forgetPassword({
      username: state.step1.account,
      email: state.step1.account,
      code: state.step1.code,
      new_password: md5(state.step2.newPassword),
    })
    if (response.data?.code === 200) {
      notification.success({
        message: '重置成功',
        description: '请使用新密码登录',
      })
      setTimeout(() => router.push('/login'), 1200)
    }
  } catch {
    /* axios 拦截器已提示 */
  } finally {
    state.loading = false
  }
}
</script>

<style lang="scss" scoped>
.login-page-root {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-image: url("/background.png");
  background-size: 100% 100%;
}

.login-auth-split {
  display: flex;
  flex: 1;
  min-height: 0;
}

.login-auth-split__col--illustration {
  flex: 0 0 58%;
  min-width: 0;
}

.login-auth-split__col--form {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  background: transparent;
}

.login-page-panel {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

.login-page-panel__main {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  padding: 48px 32px 16px;
}

.auth-right-wrap {
  width: min(440px, 100%);
  padding: 8px 0;
}

.form-intro .title {
  margin: 0;
  font-size: 28px;
  font-weight: 650;
  line-height: 1.2;
  color: rgba(0, 0, 0, 0.85);
}

.form-intro .sub-title {
  margin: 10px 0 28px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
}

.login-page-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 24px 24px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.45);

  a {
    color: rgba(0, 0, 0, 0.65);
  }
}

.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;

  .step-number {
    display: flex;
    width: 32px;
    height: 32px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #e5e7eb;
    color: #9ca3af;
    font-size: 14px;
    font-weight: 600;
  }

  .step-label {
    font-size: 12px;
    color: #9ca3af;
  }

  &.active .step-number {
    background: #1677ff;
    color: #fff;
  }

  &.active .step-label {
    color: #1677ff;
  }

  &.completed .step-number {
    background: #52c41a;
    color: #fff;
  }
}

.step-divider {
  width: 48px;
  height: 2px;
  background: #e5e7eb;
}

.email-code-row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;

  .email-code-input {
    flex: 1;
    min-width: 0;
  }

  .email-code-btn {
    flex-shrink: 0;
    min-width: 120px;
  }
}

.auth-submit-btn {
  width: 100%;
}

.step-actions {
  display: flex;
  gap: 12px;

  .ant-btn {
    flex: 1;
  }
}

.auth-footer-links {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;

  a {
    color: #1677ff;
  }
}

@media (max-width: 960px) {
  .login-auth-split {
    flex-direction: column;
  }

  .login-auth-split__col--illustration {
    flex: 0 0 auto;
    min-height: 220px;
  }
}
</style>
