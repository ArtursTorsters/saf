
import type { SensorData } from '../types/sensor'

const API_BASE: string = import.meta.env.VITE_API_BASE
const MAX_RETRIES = 3
const RETRY_DELAY_MS = 1000

const wait = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms))

export const fetchSensors = async (): Promise<SensorData> => {
  let lastError: Error | null = null

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const response = await fetch(`${API_BASE}/sensors`)

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      return response.json() as Promise<SensorData>
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err))
      console.warn(`Fetch attempt ${attempt}/${MAX_RETRIES} failed:`, lastError.message)

      if (attempt < MAX_RETRIES) {
        await wait(RETRY_DELAY_MS * attempt)
      }
    }
  }

  throw lastError ?? new Error('Failed to fetch sensors after retries')
}
