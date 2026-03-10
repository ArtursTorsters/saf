import { Ref, ComputedRef } from "vue"

export interface SensorMetrics {
  [key: string]: number | null
}

export interface Sensor {
  id: number
  name: string
  typeName: string
  metrics: SensorMetrics
}

export interface SensorData {
  sensors: Sensor[]
  metricColumns: string[]
}


export interface UseSensorsReturn {
  sensors: Ref<Sensor[]>
  metricColumns: Ref<string[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  searchQuery: Ref<string>
  selectedType: Ref<string>
  sortKey: Ref<string>
  sortOrder: Ref<SortOrder>
  visibleColumns: Ref<Set<string>>
  uniqueTypes: ComputedRef<string[]>
  filteredSensors: ComputedRef<Sensor[]>
  toggleSort: (key: string) => void
  toggleColumn: (column: string) => void
  isColumnVisible: (column: string) => boolean
  loadData: () => Promise<void>
}


export type SortOrder = 'asc' | 'desc'
