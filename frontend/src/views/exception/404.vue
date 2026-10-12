<template>
  <a-result status="404" title="404" sub-title="您访问的页面不存在">
    <template #extra>
      <a-button type="primary" @click="toHome">返回首页</a-button>
    </template>
  </a-result>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";

const router = useRouter();
const toHome = () => {
  router.push('/')
}
</script>

<style lang="scss" scoped>

</style>
