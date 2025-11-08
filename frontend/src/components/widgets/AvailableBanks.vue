<template>
  <div class="inline-grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div
      v-for="bank in AVAILABLE_BANKS"
      :key="bank.id"
      class="flex flex-col p-4 bg-card rounded-lg gap-2 border border-border shadow-sm"
    >
      <div class="flex items-center gap-2">
        <div class="size-10 inline-flex items-center justify-center rounded-md" :style="{ backgroundColor: bank.brandColor }">{{ bank.logo }}</div>
        <span class="font-medium">{{ bank.name }}</span>
      </div>
      <div class="flex gap-1 text-sm text-muted-foreground mb-2">
        <span>{{ bank.fullName }}</span>
        <span>-</span>
        <span>{{ bank.ruName }}</span>
      </div>
      <UiButton
        v-if="!isBankAdded(bank.name)"
        variant="outline"
        size="sm"
        :disabled="mapBanksToLoading[bank.name] || isGetBanksLoading"
        @click="addBank(bank)"
      >
        {{
          mapBanksToLoading[bank.name]
            ? 'Загрузка...'
            : 'Добавить'
        }}
      </UiButton>
      <UiButton
        v-else
        variant="outline"
        size="sm"
        :disabled="mapBanksToLoading[bank.name] || isGetBanksLoading"
        @click="isBankConsented(bank.name) ? rejectConsent(bank) : consentBank(bank)"
      >
        {{
          mapBanksToLoading[bank.name]
            ? 'Загрузка...'
            : isBankConsented(bank.name)
              ? 'Отозвать согласие'
              : 'Согласие на подключение'
        }}
      </UiButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { toast } from 'vue-sonner'
import { storeToRefs } from 'pinia'

import { Button as UiButton } from '@/components/ui/button'

import { ResponseError } from '@/api/runtime'

import { AVAILABLE_BANKS, CLIENT_ID, CLIENT_SECRET } from '@/shared/constants'
import { type TBank, type TBankName } from '@/shared/types'
import { EBankName } from '@/shared/enums'

import { useBanksStore } from '@/stores/banks'
import { useUserStore } from '@/stores/user'

defineOptions({
  name: 'WAvailableBanks',
})

type TMapBanksToLoading = Record<TBankName, boolean>

const mapBanksToLoading = reactive<TMapBanksToLoading>(Object.values(EBankName).reduce((acc, bank) => {
  acc[bank] = false
  return acc
}, {} as TMapBanksToLoading))

const userStore = useUserStore()
const { connectedBanks } = storeToRefs(userStore)
const banksStore = useBanksStore()
const { banks, isGetBanksLoading, mapBanksToName } = storeToRefs(banksStore)

const getUser = async () => {
  try {
    await userStore.getMe()
  } catch (error: unknown) {
    if (error instanceof ResponseError) {
      const errorData = await (error as ResponseError).response.json()

      return toast.error(errorData.detail)
    }

    toast.error('Неизвестная ошибка')
  }
}

const getBanks = async () => {
  try {
    await banksStore.getBanks()
  } catch (error) {
    if (error instanceof ResponseError) {
      const errorData = await (error as ResponseError).response.json()

      return toast.error(errorData.detail)
    }

    toast.error('Неизвестная ошибка')
  }
}

const addBank = async ({ name, apiUrl }: TBank) => {
  try {
    mapBanksToLoading[name] = true

    await banksStore.addBank({
      name,
      apiUrl,
      clientId: CLIENT_ID,
      clientSecret: CLIENT_SECRET,
    })

    getBanks()

    toast.success('Банк успешно подключен')
  } catch (error) {
    if (error instanceof ResponseError) {
      const errorData = await (error as ResponseError).response.json()

      if (errorData.detail === 'Already exists. Already exists.') {
        return toast.error('Банк уже подключен')
      }
    }
    
    toast.error('Неизвестная ошибка')
  } finally {
    mapBanksToLoading[name] = false
  }
}

const consentBank = async ({ name }: TBank) => {
  try {
    mapBanksToLoading[name] = true

    await banksStore.consentBank(mapBanksToName.value[name].id)

    getUser()

    toast.success('Согласие на подключение успешно дано')
  } catch (error) {
    if (error instanceof ResponseError) {
      const errorData = await (error as ResponseError).response.json()

      return toast.error(errorData.detail)
    }

    toast.error('Неизвестная ошибка')
  } finally {
    mapBanksToLoading[name] = false
  }
}

const rejectConsent = async ({ name }: TBank) => {
  try {
    mapBanksToLoading[name] = true

    await banksStore.rejectConsent(mapBanksToName.value[name].id)

    getUser()

    toast.success('Согласие на подключение успешно отозвано')
  } catch (error: unknown) {
    if (error instanceof ResponseError) {
      const errorData = await (error as ResponseError).response.json()

      return toast.error(errorData.detail)
    }

    toast.error('Неизвестная ошибка')
  } finally {
    mapBanksToLoading[name] = false
  }
}

const isBankAdded = (name: TBankName) => {
  return banks.value.some(b => b.name === name)
}

const isBankConsented = (name: TBankName) => {
  const bankId = mapBanksToName.value[name].id
  return connectedBanks.value.includes(bankId)
}

onMounted(getBanks)
</script>