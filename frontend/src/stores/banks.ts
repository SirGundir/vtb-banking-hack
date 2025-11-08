import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useStorage } from '@vueuse/core'

import { useApiConfig } from '@/composables/useApiConfig'

import { BankApi } from '@/api/apis/BankApi'

import { type JwtTokensDTO } from '@/api/models/JwtTokensDTO'
import { type BankSchema } from '@/api/models/BankSchema'
import { type AddBankDTO } from '@/api/models/AddBankDTO'

import { type TBankName } from '@/shared/types'

export const useBanksStore = defineStore('banks', () => {
  const accessToken = useStorage<JwtTokensDTO['accessToken'] | null>('accessToken', null)

  const banks = ref<BankSchema[]>([])
  const isGetBanksLoading = ref(false)

  const mapBanksToName = computed(() => {
    return banks.value.reduce((acc, bank) => {
      const bankName = bank.name as TBankName
      acc[bankName] = bank
      return acc
    }, {} as Record<TBankName, BankSchema>)
  })

  const getBanks = async () => {
    try {
      if (!accessToken.value) throw new Error('No access token')

      isGetBanksLoading.value = true

      const config = useApiConfig()
      const banksApi = new BankApi(config)
      const response = await banksApi.getBanksApiV1BanksGet()
      banks.value = response

      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    } finally {
      isGetBanksLoading.value = false
    }
  }

  const addBank = async (addBankDTO: AddBankDTO) => {
    try {
      if (!accessToken.value) throw new Error('No access token')

      const config = useApiConfig()
      const banksApi = new BankApi(config)
      const response = await banksApi.addBankApiV1BanksPost({ addBankDTO })

      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    }
  }

  const consentBank = async (bankId: number) => {
    try {
      if (!accessToken.value) throw new Error('No access token')

      const config = useApiConfig()
      const banksApi = new BankApi(config)
      const response = await banksApi.connectUserBankApiV1BanksBankIdAddConsentPost({ bankId })

      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    }
  }

  const rejectConsent = async (bankId: number) => {
    try {
      if (!accessToken.value) throw new Error('No access token')

      const config = useApiConfig()
      const banksApi = new BankApi(config)
      const response = await banksApi.rejectConsentApiV1BanksBankIdRejectConsentPost({ bankId })

      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    }
  }

  return {
    banks,
    isGetBanksLoading,
    mapBanksToName,
    getBanks,
    addBank,
    consentBank,
    rejectConsent,
  }
})