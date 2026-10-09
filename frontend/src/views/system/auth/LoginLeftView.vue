<template>
  <div class="login-left-view">
    <div class="login-left-view__hero">
      <div class="login-left-view__hero-ring">
        <a-image src="/logo.png" :preview="false" class="login-left-view__hero-logo" />
      </div>
    </div>
    <div class="login-left-view__desc">
      <h2>FastApiWebAdmin-Pro</h2>
      <p>完全开源的权限管理系统，支持 RBAC、动态菜单与业务插件扩展</p>
      <p class="login-left-view__desc-extra">FastApiWebAdmin-Pro 是完全开源的权限管理系统</p>
    </div>
    <div class="login-left-view__decor login-left-view__decor--circle" />
    <div class="login-left-view__decor login-left-view__decor--square" />
    <div class="login-left-view__decor login-left-view__decor--dot" />
  </div>
</template>

<script lang="ts" setup>
</script>

<style lang="scss" scoped>
.login-left-view {
  position: relative;
  display: flex;
  height: 100%;
  min-height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  overflow: hidden;
  background: transparent;
}

.login-left-view__hero {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32px;
}

.login-left-view__hero-ring {
  display: flex;
  width: 160px;
  height: 160px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgb(255 255 255 / 72%);
  box-shadow: 0 18px 40px rgb(22 119 255 / 16%);
}

.login-left-view__hero-logo {
  width: 72px;
  height: 72px;
}

.login-left-view__desc {
  max-width: 420px;
  text-align: center;
}

.login-left-view__desc h2 {
  margin: 0 0 12px;
  font-size: 28px;
  font-weight: 650;
  color: rgba(0, 0, 0, 0.85);
}

.login-left-view__desc p {
  margin: 0;
  font-size: 14px;
  line-height: 1.7;
  color: rgba(0, 0, 0, 0.45);
}

.login-left-view__desc-extra {
  margin-top: 10px !important;
}

.login-left-view__decor {
  position: absolute;
  pointer-events: none;
}

.login-left-view__decor--circle {
  top: 12%;
  left: 10%;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: rgb(22 119 255 / 8%);
}

.login-left-view__decor--square {
  right: 12%;
  bottom: 18%;
  width: 88px;
  height: 88px;
  border-radius: 18px;
  background: rgb(19 194 194 / 10%);
  transform: rotate(18deg);
}

.login-left-view__decor--dot {
  top: 28%;
  right: 22%;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: rgb(22 119 255 / 35%);
}
</style>
