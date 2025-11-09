import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

import { useApiConfig } from '@/composables/useApiConfig'
import { UsersApi, type GetMeTransactionsApiV1UsersMeTransactionsGetRequest } from '@/api/apis/UsersApi'
import { type JwtTokensDTO } from '@/api/models/JwtTokensDTO'

export const useTransactionsStore = defineStore('transactions', () => {
  const accessToken = useStorage<JwtTokensDTO['accessToken'] | null>('accessToken', null)

  const getTransactions = async (
    requestParameters?: GetMeTransactionsApiV1UsersMeTransactionsGetRequest
  ) => {
    try {
      if (!accessToken.value) throw new Error('No access token')

      const config = useApiConfig()
      const usersApi = new UsersApi(config)
      const response = await usersApi
        .getMeTransactionsApiV1UsersMeTransactionsGet(requestParameters)

      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    }
  }

  return {
    getTransactions,
  }
})