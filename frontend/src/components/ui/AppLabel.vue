<template>
  <label
    :for="htmlFor"
    class="text-xs font-semibold uppercase tracking-wider text-gray-500"
  >
    <slot />
  </label>
</template>

<script setup lang="ts">
import type { AppLabelProps } from '../../types/ui'

withDefaults(defineProps<AppLabelProps>(), {
  htmlFor: undefined,
})
</script>
