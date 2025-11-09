import { ref } from 'vue'
import { DEFAULT_START_DATE, DEFAULT_END_DATE } from '@/shared/constants'

export const useDateRangeFilter = () => {
  const startDate = ref<Date>(DEFAULT_START_DATE)
  const endDate = ref<Date>(DEFAULT_END_DATE)

  return {
    startDate,
    endDate,
  }
}
