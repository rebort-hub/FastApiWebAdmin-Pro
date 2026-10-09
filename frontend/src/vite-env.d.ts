/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_BASE_API: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<object, object, unknown>
  export default component
}

declare module 'md5' {
  function md5(message: string | number[] | Uint8Array): string
  export default md5
}

declare module 'store' {
  interface StoreJsAPI {
    get(key: string): unknown
    set(key: string, value: unknown, expires?: number): void
    remove(key: string): void
  }
  const store: StoreJsAPI
  export default store
}
