<template>
  <div class="ntesterc-logo" :class="{ 'ntesterc-logo--collapsed': collapsed }" @click="onClick">
    <img class="ntesterc-logo__img" src="/logo.png" alt="logo" />
    <transition name="ntesterc-logo-fade">
      <span v-if="!collapsed" class="ntesterc-logo__title">{{ title }}</span>
    </transition>
  </div>
</template>

<script lang="ts" setup>
defineOptions({ name: 'NtestercLogo' })

withDefaults(
  defineProps<{
    title?: string
    collapsed?: boolean
  }>(),
  {
    title: 'FastApiWebAdmin',
    collapsed: false,
  },
)

const emit = defineEmits<{
  click: []
}>()

function onClick() {
  emit('click')
}
</script>

<style lang="scss" scoped>
.ntesterc-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 0 4px;
  cursor: pointer;
  user-select: none;

  &--collapsed {
    justify-content: center;
    width: auto;
    padding: 0;
  }

  &__img {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    object-fit: contain;
  }

  &__title {
    overflow: hidden;
    font-size: 15px;
    font-weight: 600;
    line-height: 1.3;
    color: var(--ntesterc-logo-title);
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}

.ntesterc-logo-fade-enter-active,
.ntesterc-logo-fade-leave-active {
  transition: opacity 0.15s ease;
}

.ntesterc-logo-fade-enter-from,
.ntesterc-logo-fade-leave-to {
  opacity: 0;
}
</style>
