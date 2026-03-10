

import type { SensorData } from '../types/sensor'

const API_BASE: string = import.meta.env.VITE_API_BASE

export const fetchSensors = async (): Promise<SensorData> => {
  const response = await fetch(`${API_BASE}/sensors`)

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`)
  }

  return response.json() as Promise<SensorData>
}
