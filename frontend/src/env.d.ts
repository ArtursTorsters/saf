/// <reference types="vite/client" />

/**
 * Type declarations for Vite environment variables.
 * Any VITE_-prefixed var in .env is available on import.meta.env.
 */
interface ImportMetaEnv {
  readonly VITE_API_BASE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

/**
 * Allow importing .vue files as modules.
 */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<object, object, unknown>
  export default component
}
