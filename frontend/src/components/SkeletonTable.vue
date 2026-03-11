<template>
  <div class="max-w-screen-xl mx-auto px-6 py-6 animate-pulse">
    <div class="flex gap-6 mb-4">
      <div class="flex flex-col gap-1.5">
        <div class="h-3 w-12 bg-gray-800 rounded"></div>
        <div class="h-10 w-72 bg-gray-900 rounded-lg border border-gray-800"></div>
      </div>
      <div class="flex flex-col gap-1.5">
        <div class="h-3 w-20 bg-gray-800 rounded"></div>
        <div class="h-10 w-44 bg-gray-900 rounded-lg border border-gray-800"></div>
      </div>
    </div>

    <div class="flex gap-2 mb-4">
      <div v-for="i in 4" :key="i" class="h-7 w-28 bg-gray-900 rounded-full border border-gray-800"></div>
    </div>

    <div class="h-3 w-40 bg-gray-800 rounded mb-3"></div>

    <div class="border border-gray-800 rounded-xl overflow-hidden">
      <div class="bg-gray-950 px-4 py-3 flex gap-8 border-b border-gray-800">
        <div class="h-3 w-24 bg-gray-800 rounded"></div>
        <div class="h-3 w-16 bg-gray-800 rounded"></div>
        <div v-for="i in 3" :key="i" class="h-3 w-20 bg-gray-800 rounded"></div>
      </div>

      <div v-for="row in 8" :key="row" class="px-4 py-3 flex gap-8 border-b border-gray-800 last:border-b-0">
        <div class="flex flex-col gap-1">
          <div class="h-4 w-32 bg-gray-900 rounded"></div>
          <div class="h-2.5 w-20 bg-gray-900 rounded"></div>
        </div>
        <div class="h-5 w-20 bg-gray-900 rounded-full"></div>
        <div v-for="i in 3" :key="i" class="h-4 w-14 bg-gray-900 rounded ml-auto"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
