<template>
  <a-drawer
    v-model:open="open"
    title="主题设置"
    placement="right"
    :width="400"
    root-class-name="ntesterc-settings-drawer"
    :body-style="{ padding: '16px 20px 8px' }"
  >
    <div class="ntesterc-settings">
      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">主题风格</div>
        <div class="ntesterc-settings__grid ntesterc-settings__grid--3">
          <button
            v-for="item in themeOptions"
            :key="item.value"
            type="button"
            class="option-card"
            :class="{ 'is-active': draft.themeMode === item.value }"
            @click="updateDraft({ themeMode: item.value })"
          >
            <span class="option-card__preview" v-html="item.icon" />
            <span class="option-card__name">{{ item.label }}</span>
            <span class="option-card__check"><CheckOutlined /></span>
          </button>
        </div>
      </section>

      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">菜单布局</div>
        <div class="ntesterc-settings__grid ntesterc-settings__grid--4">
          <button
            v-for="item in layoutOptions"
            :key="item.value"
            type="button"
            class="option-card"
            :class="{ 'is-active': draft.menuLayout === item.value }"
            @click="updateDraft({ menuLayout: item.value })"
          >
            <span class="option-card__preview option-card__preview--layout">
              <span class="layout-wire" :class="`layout-wire--${item.value}`">
                <i /><i /><i />
              </span>
            </span>
            <span class="option-card__name">{{ item.label }}</span>
            <span class="option-card__check"><CheckOutlined /></span>
          </button>
        </div>
      </section>

      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">菜单风格</div>
        <div class="ntesterc-settings__grid ntesterc-settings__grid--5">
          <button
            v-for="item in menuStyleOptions"
            :key="item.value"
            type="button"
            class="option-card"
            :class="{ 'is-active': draft.menuStyle === item.value }"
            @click="updateDraft({ menuStyle: item.value })"
          >
            <span class="option-card__preview option-card__preview--menu">
              <span class="menu-wire" :class="`menu-wire--${item.value}`">
                <i /><i /><i />
              </span>
            </span>
            <span class="option-card__name">{{ item.label }}</span>
            <span class="option-card__check"><CheckOutlined /></span>
          </button>
        </div>
      </section>

      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">系统主题色</div>
        <div class="ntesterc-settings__colors">
          <button
            v-for="c in NTESTERC_PRESET_COLORS"
            :key="c"
            type="button"
            class="color-dot"
            :class="{ 'is-active': draft.primaryColor === c }"
            :style="{ background: c }"
            @click="updateDraft({ primaryColor: c })"
          >
            <CheckOutlined v-if="draft.primaryColor === c" />
          </button>
          <div class="color-custom">
            <label class="color-dot color-dot--custom" title="自定义">
              <input type="color" :value="draft.primaryColor" @input="onCustomColor" />
            </label>
            <span>自定义</span>
          </div>
        </div>
      </section>

      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">盒子样式</div>
        <div class="ntesterc-settings__grid ntesterc-settings__grid--2">
          <button
            type="button"
            class="option-card option-card--box"
            :class="{ 'is-active': draft.boxStyle === 'border' }"
            @click="updateDraft({ boxStyle: 'border' })"
          >
            <BorderOutlined class="option-card__icon" />
            <span class="option-card__name">边框</span>
            <span class="option-card__check"><CheckOutlined /></span>
          </button>
          <button
            type="button"
            class="option-card option-card--box"
            :class="{ 'is-active': draft.boxStyle === 'shadow' }"
            @click="updateDraft({ boxStyle: 'shadow' })"
          >
            <CloudOutlined class="option-card__icon" />
            <span class="option-card__name">阴影</span>
            <span class="option-card__check"><CheckOutlined /></span>
          </button>
        </div>
      </section>

      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">容器宽度</div>
        <div class="ntesterc-settings__width">
          <button
            type="button"
            class="width-card"
            :class="{ 'is-active': draft.containerWidth === 'full' }"
            @click="updateDraft({ containerWidth: 'full' })"
          >
            <ExpandOutlined />
            <span>铺满</span>
            <span class="option-card__check"><CheckOutlined /></span>
          </button>
          <div
            class="width-card width-card--fixed"
            :class="{ 'is-active': draft.containerWidth === 'fixed' }"
            @click="updateDraft({ containerWidth: 'fixed' })"
          >
            <ColumnWidthOutlined />
            <span>定宽</span>
            <a-input-number
              :value="draft.containerFixedWidth"
              :min="960"
              :max="1920"
              :step="20"
              addon-after="px"
              @click.stop
              @change="onFixedWidthChange"
            />
            <span class="option-card__check"><CheckOutlined /></span>
          </div>
        </div>
      </section>

      <section class="ntesterc-settings__section">
        <div class="ntesterc-settings__title">基础配置</div>
        <div class="ntesterc-settings__rows">
          <div class="ntesterc-settings__row">
            <span>页面动画</span>
            <a-switch
              :checked="draft.enablePageAnimation"
              @change="(v: boolean) => updateDraft({ enablePageAnimation: v })"
            />
          </div>
          <div class="ntesterc-settings__row">
            <span>显示面包屑</span>
            <a-switch
              :checked="draft.showBreadcrumb"
              @change="(v: boolean) => updateDraft({ showBreadcrumb: v })"
            />
          </div>
          <div class="ntesterc-settings__row">
            <span>页面切换动画</span>
            <a-select
              :value="draft.pageTransition"
              style="width: 108px"
              :options="NTESTERC_PAGE_TRANSITIONS"
              @change="(v: NtestercPageTransition) => updateDraft({ pageTransition: v })"
            />
          </div>
          <div class="ntesterc-settings__row">
            <span>页面加载进度条</span>
            <a-switch
              :checked="draft.showNprogress"
              @change="(v: boolean) => updateDraft({ showNprogress: v })"
            />
          </div>
          <div class="ntesterc-settings__row">
            <span>多标签页</span>
            <a-switch
              :checked="draft.showWorkTab"
              @change="(v: boolean) => updateDraft({ showWorkTab: v })"
            />
          </div>
        </div>
      </section>
    </div>

    <template #footer>
      <div class="ntesterc-settings__footer">
        <a-button @click="onReset">重置为默认</a-button>
        <div class="ntesterc-settings__footer-actions">
          <a-button @click="onCancel">取消</a-button>
          <a-button type="primary" @click="onSave">保存设置</a-button>
        </div>
      </div>
    </template>
  </a-drawer>
</template>

<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import {
  BorderOutlined,
  CheckOutlined,
  CloudOutlined,
  ColumnWidthOutlined,
  ExpandOutlined,
} from '@ant-design/icons-vue'
import { useNtestercSettings } from '@/composables/useNtestercSettings'
import {
  DEFAULT_APP_SETTINGS,
  NTESTERC_PAGE_TRANSITIONS,
  NTESTERC_PRESET_COLORS,
  type NtestercAppSettings,
  type NtestercMenuLayout,
  type NtestercMenuStyle,
  type NtestercPageTransition,
} from '@/types/app'
import type { NtestercThemeMode } from '@/composables/useNtestercTheme'

defineOptions({ name: 'NtestercSettingsPanel' })

const props = defineProps<{
  modelValue?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const open = ref(props.modelValue ?? false)
const { settings, patchSettings, persistSettings, restoreSettings, resetSettings } =
  useNtestercSettings()

const draft = reactive<NtestercAppSettings>({ ...settings.value })
let snapshot: NtestercAppSettings = { ...settings.value }

const themeOptions: { value: NtestercThemeMode; label: string; icon: string }[] = [
  {
    value: 'light',
    label: '浅色',
    icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M3 12h2M19 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
  },
  {
    value: 'dark',
    label: '深色',
    icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4 7 7 0 0 0 20 14.5z"/></svg>',
  },
  {
    value: 'auto',
    label: '跟随系统',
    icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>',
  },
]

const layoutOptions: { value: NtestercMenuLayout; label: string }[] = [
  { value: 'vertical', label: '垂直' },
  { value: 'horizontal', label: '水平' },
  { value: 'mixed', label: '混合' },
  { value: 'dual', label: '双列' },
]

const menuStyleOptions: { value: NtestercMenuStyle; label: string }[] = [
  { value: 'simple', label: '简约' },
  { value: 'card', label: '卡片' },
  { value: 'outline', label: '描边' },
  { value: 'immersive', label: '沉浸' },
  { value: 'glass', label: '毛玻璃' },
]

watch(
  () => props.modelValue,
  (v) => {
    if (v !== undefined) open.value = v
  },
)

watch(open, (v) => {
  emit('update:modelValue', v)
  if (v) {
    snapshot = { ...settings.value }
    Object.assign(draft, snapshot)
  }
})

function updateDraft(partial: Partial<NtestercAppSettings>) {
  Object.assign(draft, partial)
  patchSettings(partial, false)
}

function onCustomColor(e: Event) {
  const value = (e.target as HTMLInputElement).value
  updateDraft({ primaryColor: value })
}

function onFixedWidthChange(value: number | string | null) {
  const next = Number(value) || 1200
  updateDraft({ containerWidth: 'fixed', containerFixedWidth: next })
}

function onReset() {
  Object.assign(draft, DEFAULT_APP_SETTINGS)
  resetSettings()
  snapshot = { ...DEFAULT_APP_SETTINGS }
  message.success('已重置为默认设置')
}

function onCancel() {
  restoreSettings(snapshot)
  Object.assign(draft, snapshot)
  open.value = false
}

function onSave() {
  persistSettings()
  snapshot = { ...settings.value }
  message.success('设置已保存')
  open.value = false
}
</script>

<style lang="scss" scoped>
.ntesterc-settings {
  &__section {
    margin-bottom: 22px;
  }

  &__title {
    margin-bottom: 10px;
    font-size: 13px;
    font-weight: 600;
    color: var(--ntesterc-text);
  }

  &__grid {
    display: grid;
    gap: 10px;

    &--2 {
      grid-template-columns: repeat(2, 1fr);
    }

    &--3 {
      grid-template-columns: repeat(3, 1fr);
    }

    &--4 {
      grid-template-columns: repeat(4, 1fr);
    }

    &--5 {
      grid-template-columns: repeat(5, 1fr);
    }
  }

  &__colors {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
  }

  &__rows {
    border-top: 1px solid var(--ntesterc-border);
  }

  &__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 44px;
    font-size: 13px;
    color: var(--ntesterc-text-secondary);
    border-bottom: 1px solid var(--ntesterc-border);
  }

  &__width {
    display: grid;
    grid-template-columns: 1fr 1.6fr;
    gap: 10px;
  }

  &__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__footer-actions {
    display: flex;
    gap: 8px;
  }
}

.option-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 72px;
  padding: 8px 4px 6px;
  cursor: pointer;
  background: var(--ntesterc-menu-hover);
  border: 1.5px solid var(--ntesterc-border);
  border-radius: 8px;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;

  &:hover {
    border-color: color-mix(in srgb, var(--ntesterc-primary) 35%, var(--ntesterc-border));
  }

  &.is-active {
    background: color-mix(in srgb, var(--ntesterc-primary) 8%, transparent);
    border-color: var(--ntesterc-primary);
    box-shadow: 0 0 0 1px color-mix(in srgb, var(--ntesterc-primary) 18%, transparent);

    .option-card__check {
      opacity: 1;
      transform: scale(1);
    }

    .option-card__icon,
    .option-card__preview :deep(.anticon) {
      color: var(--ntesterc-primary);
    }
  }

  &__preview {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 28px;
    font-size: 20px;
    color: var(--ntesterc-text-secondary);

    :deep(svg) {
      display: block;
    }
  }

  &__name {
    margin-top: 4px;
    font-size: 12px;
    line-height: 18px;
    color: var(--ntesterc-text);
  }

  &__icon {
    font-size: 22px;
    color: var(--ntesterc-text-secondary);
  }

  &--box {
    height: 72px;
  }

  &__check {
    position: absolute;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    font-size: 10px;
    color: #fff;
    background: var(--ntesterc-primary);
    border-radius: 8px 0 6px;
    opacity: 0;
    transform: scale(0.6);
    transition:
      opacity 0.2s,
      transform 0.2s;
  }
}

.color-dot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  color: #fff;
  cursor: pointer;
  border: none;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px rgb(0 0 0 / 6%);

  &.is-active {
    box-shadow:
      0 0 0 2px var(--ntesterc-card-bg),
      0 0 0 3.5px var(--ntesterc-primary);
  }

  &--custom {
    position: relative;
    overflow: hidden;
    background: conic-gradient(
      from 180deg,
      #ff6b6b,
      #feca57,
      #48dbfb,
      #ff9ff3,
      #54a0ff,
      #5f27cd,
      #ff6b6b
    );

    input {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      cursor: pointer;
      opacity: 0;
    }
  }

  :deep(.anticon) {
    font-size: 12px;
  }
}

.width-card {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: center;
  min-height: 64px;
  padding: 8px 10px;
  cursor: pointer;
  background: var(--ntesterc-menu-hover);
  border: 1.5px solid var(--ntesterc-border);
  border-radius: 8px;
  transition: border-color 0.2s;

  &.is-active {
    border-color: var(--ntesterc-primary);

    .option-card__check {
      opacity: 1;
      transform: scale(1);
    }
  }

  &--fixed {
    justify-content: flex-start;
  }

  > span {
    font-size: 13px;
    color: var(--ntesterc-text);
  }

  :deep(.ant-input-number) {
    width: 118px;
    margin-left: auto;
  }
}

.layout-wire {
  display: grid;
  width: 42px;
  height: 28px;
  overflow: hidden;
  background: color-mix(in srgb, var(--ntesterc-primary) 12%, #fff);
  border-radius: 4px;

  &--vertical {
    grid-template-columns: 10px 1fr;
    gap: 3px;
    padding: 3px;

    i:nth-child(1) {
      grid-row: 1 / 3;
      background: color-mix(in srgb, var(--ntesterc-primary) 45%, #fff);
    }

    i:nth-child(2),
    i:nth-child(3) {
      height: 6px;
      background: color-mix(in srgb, var(--ntesterc-primary) 28%, #fff);
      border-radius: 2px;
    }
  }

  &--horizontal {
    grid-template-rows: 7px 1fr;
    gap: 3px;
    padding: 3px;

    i:nth-child(1) {
      background: color-mix(in srgb, var(--ntesterc-primary) 45%, #fff);
    }

    i:nth-child(2) {
      background: color-mix(in srgb, var(--ntesterc-primary) 22%, #fff);
    }

    i:nth-child(3) {
      display: none;
    }
  }

  &--mixed {
    grid-template-columns: 10px 1fr;
    grid-template-rows: 7px 1fr;
    gap: 3px;
    padding: 3px;

    i:nth-child(1) {
      grid-column: 1 / 3;
      background: color-mix(in srgb, var(--ntesterc-primary) 45%, #fff);
    }

    i:nth-child(2) {
      background: color-mix(in srgb, var(--ntesterc-primary) 38%, #fff);
    }

    i:nth-child(3) {
      background: color-mix(in srgb, var(--ntesterc-primary) 22%, #fff);
    }
  }

  &--dual {
    grid-template-columns: 7px 10px 1fr;
    gap: 2px;
    padding: 3px;

    i {
      background: color-mix(in srgb, var(--ntesterc-primary) 28%, #fff);
    }

    i:nth-child(1) {
      background: color-mix(in srgb, var(--ntesterc-primary) 50%, #fff);
    }

    i:nth-child(3) {
      background: color-mix(in srgb, var(--ntesterc-primary) 18%, #fff);
    }
  }

  i {
    display: block;
    border-radius: 2px;
  }
}

.menu-wire {
  display: flex;
  flex-direction: column;
  gap: 3px;
  width: 36px;

  i {
    display: block;
    height: 5px;
    background: color-mix(in srgb, var(--ntesterc-primary) 35%, #fff);
  }

  &--simple i {
    border-radius: 1px;
  }

  &--card i {
    height: 7px;
    background: #fff;
    border: 1px solid color-mix(in srgb, var(--ntesterc-primary) 40%, #fff);
    border-radius: 2px;
  }

  &--outline i {
    background: transparent;
    border: 1px solid color-mix(in srgb, var(--ntesterc-primary) 50%, #fff);
    border-radius: 1px;
  }

  &--immersive i:first-child {
    background: var(--ntesterc-primary);
  }

  &--glass i {
    background: color-mix(in srgb, var(--ntesterc-primary) 18%, transparent);
    border: 1px solid color-mix(in srgb, var(--ntesterc-primary) 28%, transparent);
    backdrop-filter: blur(4px);
  }
}

.color-custom {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  gap: 6px;

  span {
    font-size: 12px;
    line-height: 1;
    color: var(--ntesterc-text-secondary);
    white-space: nowrap;
  }
}
</style>
