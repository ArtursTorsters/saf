<template>
  <select
    :id="id"
    :value="modelValue"
    class="bg-transparent border border-gray-700 rounded-lg text-white text-sm px-3 py-2.5 min-w-[180px] cursor-pointer transition-colors duration-200 focus:outline-none focus:border-gray-400"
    v-bind="$attrs"
    @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
  >
    <slot />
  </select>
</template>

<script setup lang="ts">
import type { AppSelectProps, AppSelectEmits } from '../../types/ui'

withDefaults(defineProps<AppSelectProps>(), {
  modelValue: '',
  id: undefined,
})

defineEmits<AppSelectEmits>()
</script>
