import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchSensors } from '../services/api'
import type { Sensor, SortOrder } from '../types/sensor'

export const useSensorStore = defineStore('sensors', () => {
  const sensors = ref<Sensor[]>([])
  const metricColumns = ref<string[]>([])
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const hasFetched = ref<boolean>(false)

  const searchQuery = ref<string>('')
  const selectedType = ref<string>('')
  const sortKey = ref<string>('name')
  const sortOrder = ref<SortOrder>('asc')
  const visibleColumns = ref<Set<string>>(new Set())

  const uniqueTypes = computed<string[]>(() => {
    const types = sensors.value
      .map((s) => s.typeName)
      .filter(Boolean)
    return [...new Set(types)].sort()
  })

  const filteredSensors = computed<Sensor[]>(() => {
    let result = [...sensors.value]

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter((s) =>
        s.name.toLowerCase().includes(query)
      )
    }

    if (selectedType.value) {
      result = result.filter((s) => s.typeName === selectedType.value)
    }

    result.sort((a, b) => {
      let valA: string | number
      let valB: string | number

      if (sortKey.value === 'name' || sortKey.value === 'typeName') {
        valA = (a[sortKey.value] || '').toLowerCase()
        valB = (b[sortKey.value] || '').toLowerCase()
      } else {
        const rawA = a.metrics[sortKey.value]
        const rawB = b.metrics[sortKey.value]
        valA = rawA === null || rawA === undefined
          ? (sortOrder.value === 'asc' ? Infinity : -Infinity)
          : rawA
        valB = rawB === null || rawB === undefined
          ? (sortOrder.value === 'asc' ? Infinity : -Infinity)
          : rawB
      }

      if (valA < valB) return sortOrder.value === 'asc' ? -1 : 1
      if (valA > valB) return sortOrder.value === 'asc' ? 1 : -1
      return 0
    })

    return result
  })

  const toggleSort = (key: string): void => {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
      sortKey.value = key
      sortOrder.value = 'asc'
    }
  }

  const toggleColumn = (column: string): void => {
    const newSet = new Set(visibleColumns.value)
    if (newSet.has(column)) {
      newSet.delete(column)
    } else {
      newSet.add(column)
    }
    visibleColumns.value = newSet
  }

  const isColumnVisible = (column: string): boolean => {
    return visibleColumns.value.has(column)
  }

  const loadData = async (): Promise<void> => {
    loading.value = true
    error.value = null
    try {
      const data = await fetchSensors()
      sensors.value = data.sensors
      metricColumns.value = data.metricColumns
      visibleColumns.value = new Set(data.metricColumns)
      hasFetched.value = true
    } catch (err) {
      error.value = err instanceof Error ? err.message : String(err)
      console.error('Failed to load sensor data:', err)
    } finally {
      loading.value = false
    }
  }

  const loadIfNeeded = async (): Promise<void> => {
    if (!hasFetched.value) {
      await loadData()
    }
  }

  return {
    sensors,
    metricColumns,
    loading,
    error,
    hasFetched,
    searchQuery,
    selectedType,
    sortKey,
    sortOrder,
    visibleColumns,
    uniqueTypes,
    filteredSensors,
    toggleSort,
    toggleColumn,
    isColumnVisible,
    loadData,
    loadIfNeeded,
  }
})
