
import { onMounted } from 'vue'
import { useSensorStore } from '../stores/sensorStore'

export const useSensors = () => {
  const store = useSensorStore()

  onMounted(() => {
    store.loadIfNeeded()
  })

  return store
}
