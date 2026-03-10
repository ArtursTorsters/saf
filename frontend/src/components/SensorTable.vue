<template>
  <div class="font-sans bg-black text-white min-h-screen">

    <header class="border-b border-gray-800 px-8 pt-8 pb-6">
      <h1 class="text-2xl font-bold tracking-tight">Sensor Dashboard</h1>
      <p class="mt-1 text-sm text-gray-500">Real-time sensor measurement data</p>
    </header>

    <div v-if="loading" class="flex flex-col items-center justify-center py-24 text-gray-500">
      <div class="w-8 h-8 border-2 border-gray-800 border-t-white rounded-full animate-spin mb-4"></div>
      <p>Loading sensor data...</p>
    </div>

    <div v-else-if="error" class="text-center py-16">
      <p class="text-lg font-medium text-gray-400 mb-2">Something went wrong</p>
      <p class="text-red-400 mb-6 text-sm">{{ error }}</p>
      <AppButton variant="primary" @click="loadData">Retry</AppButton>
    </div>

    <div v-else class="max-w-screen-xl mx-auto px-6 py-6">

      <div class="flex gap-6 mb-4 flex-wrap">
        <div class="flex flex-col gap-1.5">
          <AppLabel html-for="search-input">Search</AppLabel>
          <AppInput
            id="search-input"
            v-model="searchQuery"
            placeholder="Search by sensor name..."
            clearable
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <AppLabel html-for="type-filter">Filter by Type</AppLabel>
          <AppSelect id="type-filter" v-model="selectedType">
            <option value="">All Types</option>
            <option
              v-for="type in uniqueTypes"
              :key="type"
              :value="type"
            >{{ type }}</option>
          </AppSelect>
        </div>
      </div>

      <div class="flex items-center gap-3 mb-4 flex-wrap">
        <span class="text-xs font-semibold uppercase tracking-wider text-gray-500 whitespace-nowrap">
          Metrics Columns:
        </span>
        <div class="flex gap-2 flex-wrap">
          <label
            v-for="col in metricColumns"
            :key="col"
            :class="[
              'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs cursor-pointer select-none border transition-all duration-200',
              isColumnVisible(col)
                ? 'bg-white text-black border-white'
                : 'bg-transparent text-gray-500 border-gray-700 hover:border-gray-500'
            ]"
          >
            <input
              type="checkbox"
              :checked="isColumnVisible(col)"
              class="hidden"
              @change="toggleColumn(col)"
            />
            <span>{{ col }}</span>
          </label>
        </div>
      </div>

      <div class="text-xs text-gray-500 mb-3">
        Showing <strong class="text-gray-300">{{ filteredSensors.length }}</strong> of
        <strong class="text-gray-300">{{ sensors.length }}</strong> sensors
      </div>

      <div class="border border-gray-800 rounded-xl overflow-x-auto">
        <table class="w-full border-collapse whitespace-nowrap">
          <thead>
            <tr>
              <th
                class="bg-gray-950 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 border-b border-gray-800 cursor-pointer select-none hover:text-white transition-colors duration-200"
                :class="{ 'text-white': sortKey === 'name' }"
                @click="toggleSort('name')"
              >
                <span class="inline-flex items-center gap-2">
                  Sensor Name
                  <span class="text-[0.65rem] opacity-40" :class="{ 'opacity-100': sortKey === 'name' }">
                    {{ sortKey === 'name' ? (sortOrder === 'asc' ? '▲' : '▼') : '⇅' }}
                  </span>
                </span>
              </th>

              <th
                class="bg-gray-950 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 border-b border-gray-800 cursor-pointer select-none hover:text-white transition-colors duration-200"
                :class="{ 'text-white': sortKey === 'typeName' }"
                @click="toggleSort('typeName')"
              >
                <span class="inline-flex items-center gap-2">
                  Type
                  <span class="text-[0.65rem] opacity-40" :class="{ 'opacity-100': sortKey === 'typeName' }">
                    {{ sortKey === 'typeName' ? (sortOrder === 'asc' ? '▲' : '▼') : '⇅' }}
                  </span>
                </span>
              </th>

              <th
                v-for="col in visibleMetricColumns"
                :key="col"
                class="bg-gray-950 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 border-b border-gray-800 cursor-pointer select-none hover:text-white transition-colors duration-200"
                :class="{ 'text-white': sortKey === col }"
                @click="toggleSort(col)"
              >
                <span class="inline-flex items-center gap-2">
                  {{ col }}
                  <span class="text-[0.65rem] opacity-40" :class="{ 'opacity-100': sortKey === col }">
                    {{ sortKey === col ? (sortOrder === 'asc' ? '▲' : '▼') : '⇅' }}
                  </span>
                </span>
              </th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredSensors.length === 0">
              <td
                :colspan="2 + visibleMetricColumns.length"
                class="text-center py-12 text-gray-600 italic"
              >
                No sensors match your search criteria
              </td>
            </tr>

            <tr
              v-for="sensor in filteredSensors"
              :key="sensor.id"
              class="border-b border-gray-800 last:border-b-0 hover:bg-gray-950 transition-colors duration-200"
            >
              <td class="px-4 py-3">
                <div class="flex flex-col gap-0.5">
                  <span class="font-medium text-sm text-white">{{ sensor.name }}</span>
                  <span class="text-[0.65rem] text-gray-600 font-mono">ID: {{ sensor.id }}</span>
                </div>
              </td>

              <td class="px-4 py-3">
                <span
                  :class="[
                    'inline-block px-2.5 py-0.5 rounded-full text-xs font-medium border',
                    sensor.typeName === 'Unknown Type'
                      ? 'text-gray-500 border-gray-700'
                      : 'text-gray-300 border-gray-600'
                  ]"
                >
                  {{ sensor.typeName }}
                </span>
              </td>

              <td
                v-for="col in visibleMetricColumns"
                :key="col"
                class="px-4 py-3 text-right text-sm tabular-nums"
              >
                <span v-if="sensor.metrics[col] !== null && sensor.metrics[col] !== undefined">
                  {{ sensor.metrics[col] }}
                </span>
                <span v-else class="text-gray-700 italic text-xs">N/A</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useSensors } from '../composables/useSensors'

const store = useSensors()
const {
  sensors,
  metricColumns,
  loading,
  error,
  searchQuery,
  selectedType,
  sortKey,
  sortOrder,
  uniqueTypes,
  filteredSensors,
} = storeToRefs(store)
const { toggleSort, toggleColumn, isColumnVisible, loadData } = store

const visibleMetricColumns = computed(() =>
  metricColumns.value.filter((col: string) => isColumnVisible(col))
)
</script>
