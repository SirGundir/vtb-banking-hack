import { ref, watch } from 'vue'
import { toast } from 'vue-sonner'

import { ResponseError } from '@/api/runtime'

import { useDateRangeFilter } from '@/composables/useDateRangeFilter'

import { useTransactionsStore } from '@/stores/transactions'
import { type UserTransactionsSchema } from '@/api/models/UserTransactionsSchema'

export const useMyTransactions = () => {
  const transactions = ref<UserTransactionsSchema[]>([])
  const isGetTransactionsLoading = ref(false)

  const transactionsStore = useTransactionsStore()
  const { startDate, endDate } = useDateRangeFilter()

  const getMyTransactions = async () => {
    try {
      isGetTransactionsLoading.value = true
  
      const response = await transactionsStore.getTransactions({
        dateFrom: startDate.value ? new Date(startDate.value) : undefined,
        dateTo: endDate.value ? new Date(endDate.value) : undefined,
      })
  
      transactions.value = response
    } catch (error: unknown) {
      if (error instanceof ResponseError) {
        const errorData = await (error as ResponseError).response.json()
  
        return toast.error(errorData.detail)
      }
  
      toast.error('Неизвестная ошибка')
    } finally {
      isGetTransactionsLoading.value = false
    }
  }

  watch([startDate, endDate], ([newStartDate, newEndDate]) => {
    if (newStartDate && newEndDate) {
      getMyTransactions()
    }
  }, { immediate: true })

  return {
    startDate,
    endDate,
    transactions,
    isGetTransactionsLoading,
    getMyTransactions,
  }
}
