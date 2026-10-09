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
                <div class="header">
                  <div class="logo">
                    <a-image src="/logo.png" :preview="false" />
                  </div>
                  <div class="title">欢迎回来！</div>
                </div>
              </div>

              <div class="login-main">
                <a-tabs>
                  <a-tab-pane :key="1" tab="账户密码登录">
                    <a-form
                      :model="loginForm"
                      name="normal_login"
                      class="login-form"
                      @finish="onFinish"
                    >
                      <a-form-item name="username" :rules="[{ required: true, message: '用户名是必填项！' }]">
                        <a-input v-model:value="loginForm.username" placeholder="请输入用户名">
                          <template #prefix>
                            <UserOutlined class="site-form-item-icon" />
                          </template>
                        </a-input>
                      </a-form-item>

                      <a-form-item name="password" :rules="[{ required: true, message: '密码是必填项！' }]">
                        <a-input-password v-model:value="loginForm.password" placeholder="请输入密码">
                          <template #prefix>
                            <LockOutlined class="site-form-item-icon" />
                          </template>
                        </a-input-password>
                      </a-form-item>

                      <a-form-item name="captcha" :rules="[{ required: captchaState.enable, message: '验证码是必填项！' }]">
                        <a-input v-model:value="loginForm.captcha" placeholder="验证码">
                          <template #addonAfter>
                            <div class="login-form-captcha" @click="requestCaptcha">
                              <a-image :src="captchaState.img_base" :preview="false" />
                            </div>
                          </template>
                        </a-input>
                      </a-form-item>

                      <a-form-item>
                        <a-form-item name="remember" no-style>
                          <a-checkbox v-model:checked="loginForm.remember">记住我</a-checkbox>
                        </a-form-item>
                        <router-link class="login-form-forgot" to="/forget-password">忘记密码 ?</router-link>
                      </a-form-item>

                      <a-form-item>
                        <a-button
                          type="primary"
                          html-type="submit"
                          class="login-form-button"
                          :loading="loginFlag"
                        >
                          登录
                        </a-button>
                      </a-form-item>
                    </a-form>
                  </a-tab-pane>
                </a-tabs>
              </div>
            </div>
          </div>

          <footer class="login-page-footer">
            <div class="footer-list">
              <a-button
                type="link"
                href="https://github.com/rebort-hub/FastApiWebAdmin-Pro"
                target="_blank"
              >
                <GithubOutlined />
                FastApiWebAdmin-Pro
              </a-button>
            </div>
            <div class="footer-copyright">
              <icon-font type="icon-copyright" :style="{ fontSize: '16px' }" />
              Powered by rebort-hub
            </div>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { UserOutlined, LockOutlined, GithubOutlined } from '@ant-design/icons-vue';
import { login, getCaptcha } from "@/api/auth"
import type { loginFormType, captchaStateType } from './types';
import { save_token } from "@/utils/util"
import md5 from "md5"
import LoginLeftView from "./LoginLeftView.vue"

const router = useRouter()
const loginFlag = ref(false);

const loginForm = reactive<loginFormType>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true
});

const captchaState = reactive<captchaStateType>({
  enable: true,
  key: "",
  img_base: ""
});

const onFinish = (values: loginFormType) => {
  loginFlag.value = true;

  values.password = md5(values.password);
  values.captcha_key = captchaState.key;
  login(values).then(response => {
    let result = response.data;
    if (result.code === 200) {
      save_token(result.data.access_token, result.data.refresh_token, result.data.expires_in)
      loginFlag.value = false;
      router.push('/');
    } else {
      loginFlag.value = false;
    }
  }).catch(error => {
    if (error.data?.code === 410) {
      requestCaptcha();
    }
    loginFlag.value = false;
  })
};

const requestCaptcha = () => {
  getCaptcha().then(response => {
    let result = response.data;
    if (result.code === 200) {
      captchaState.key = result.data.key;
      captchaState.img_base = result.data.img_base;
    } else {
      captchaState.enable = false;
    }
  }).catch(() => {
    captchaState.enable = false;
  })
}

onMounted(() => requestCaptcha());
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
  width: min(380px, 100%);
  padding: 8px 0;
}

.form-intro {
  .header {
    display: flex;
    line-height: 44px;
    justify-content: center;
    align-items: center;
    margin-bottom: 28px;

    .logo {
      width: 44px;
      height: 44px;
      margin-inline-end: 16px;
    }

    .title {
      font-size: 28px;
      font-weight: 650;
    }
  }
}

.login-main {
  width: 100%;
  margin: 0 auto;
}

.login-form-button {
  width: 100%;
}

.login-form-captcha {
  width: 80px;

  &:hover {
    cursor: pointer;
  }
}

.login-form-forgot {
  float: right;
}

.login-page-footer {
  padding: 16px 24px 24px;
  text-align: center;
}

.footer-list {
  .ant-btn-link {
    color: rgba(0, 0, 0, 0.65);
    margin-inline-end: 8px;
    padding: 0;
  }
}

.footer-copyright {
  margin-top: 8px;
  color: rgba(0, 0, 0, 0.45);
}

:deep(.ant-input-group .ant-input-group-addon) {
  padding: 0;
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
