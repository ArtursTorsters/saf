<template>
  <button
    :class="[
      'px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer',
      variant === 'primary'
        ? 'bg-white text-black hover:bg-gray-200 active:bg-gray-300'
        : 'bg-transparent text-gray-300 border border-gray-700 hover:border-gray-400 hover:text-white'
    ]"
    :type="type"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import type { AppButtonProps } from '../../types/ui'

withDefaults(defineProps<AppButtonProps>(), {
  variant: 'primary',
  type: 'button',
})
</script>
