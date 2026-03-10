<template>
  <div class="relative flex items-center">
    <input
      :id="id"
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      class="w-72 bg-transparent border border-gray-700 rounded-lg text-white text-sm px-3 py-2.5 pr-9 placeholder-gray-600 transition-colors duration-200 focus:outline-none focus:border-gray-400"
      v-bind="$attrs"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"/>
    <button
      v-if="clearable && modelValue"
      class="absolute right-2 bg-transparent border-none text-gray-600 hover:text-white cursor-pointer text-sm p-1 rounded transition-colors duration-200"
      type="button"
      title="Clear"
      @click="$emit('update:modelValue', '')"
    >&times;</button>
  </div>
</template>

<script setup lang="ts">
import type { AppInputProps, AppInputEmits } from '../../types/ui'

withDefaults(defineProps<AppInputProps>(), {
  modelValue: '',
  id: undefined,
  type: 'text',
  placeholder: '',
  clearable: false,
})

defineEmits<AppInputEmits>()
</script>
