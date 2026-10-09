<template>
  <main class="ntesterc-page-content">
    <div class="ntesterc-page-content__inner">
      <router-view v-slot="{ Component, route: currentRoute }">
        <transition :name="transitionName">
          <keep-alive :include="keepAliveInclude">
            <component
              :is="Component"
              v-if="Component"
              :key="currentRoute.fullPath"
              class="ntesterc-page-content__view"
            />
          </keep-alive>
        </transition>
      </router-view>
    </div>
  </main>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import type { RootState } from '@/types/store'
import { useNtestercWorkTabRouteSync } from '@/composables/useNtestercWorkTab'
import { useNtestercSettings } from '@/composables/useNtestercSettings'

defineOptions({ name: 'NtestercPageContent' })

useNtestercWorkTabRouteSync()

const store = useStore<RootState>()
const { settings } = useNtestercSettings()
const keepAliveInclude = computed(() => store.getters['worktab/keepAliveInclude'] as string[])

const transitionName = computed(() => {
  if (!settings.value.enablePageAnimation) return 'ntesterc-page-none'
  return `ntesterc-page-${settings.value.pageTransition}`
})
</script>

<style lang="scss" scoped>
.ntesterc-page-content {
  flex: 1;
  min-height: 0;
  padding: 16px 20px 32px;
  overflow: auto;
  scroll-padding-bottom: 24px;
  background: var(--ntesterc-bg);

  &__inner {
    width: 100%;
    max-width: var(--ntesterc-container-width, 100%);
    margin: 0 auto;
  }

  &__view {
    min-height: 0;
  }
}
</style>

<style lang="scss">
.ntesterc-page-none-enter-active,
.ntesterc-page-none-leave-active {
  transition: none !important;
}

.ntesterc-page-fade-enter-active,
.ntesterc-page-fade-leave-active,
.ntesterc-page-slide-left-enter-active,
.ntesterc-page-slide-left-leave-active,
.ntesterc-page-slide-bottom-enter-active,
.ntesterc-page-slide-bottom-leave-active,
.ntesterc-page-slide-top-enter-active,
.ntesterc-page-slide-top-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.ntesterc-page-fade-enter-from,
.ntesterc-page-fade-leave-to,
.ntesterc-page-slide-left-enter-from,
.ntesterc-page-slide-left-leave-to,
.ntesterc-page-slide-bottom-enter-from,
.ntesterc-page-slide-bottom-leave-to,
.ntesterc-page-slide-top-enter-from,
.ntesterc-page-slide-top-leave-to {
  opacity: 0;
}

.ntesterc-page-fade-enter-to,
.ntesterc-page-fade-leave-from,
.ntesterc-page-slide-left-enter-to,
.ntesterc-page-slide-left-leave-from,
.ntesterc-page-slide-bottom-enter-to,
.ntesterc-page-slide-bottom-leave-from,
.ntesterc-page-slide-top-enter-to,
.ntesterc-page-slide-top-leave-from {
  opacity: 1;
}

.ntesterc-page-slide-left-enter-from {
  transform: translateX(16px);
}

.ntesterc-page-slide-left-leave-to {
  transform: translateX(-16px);
}

.ntesterc-page-slide-bottom-enter-from {
  transform: translateY(16px);
}

.ntesterc-page-slide-bottom-leave-to {
  transform: translateY(-8px);
}

.ntesterc-page-slide-top-enter-from {
  transform: translateY(-16px);
}

.ntesterc-page-slide-top-leave-to {
  transform: translateY(8px);
}
</style>
