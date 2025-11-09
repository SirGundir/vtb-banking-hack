<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
        variant="outline"
        size="sm"
        :disabled="getBankButtonDisabled(bank.name)"
        @click="getBankButtonClick(bank.name)(bank)"
      >
        {{ getBankButtonText(bank.name) }}
      </UiButton>
    </div>
    <WAccountConsentsDialog
      v-if="processingBank"
      v-model:open="showAccountConsentsDialog"
      :bank-name="processingBank.name"
      :loading="mapBanksToLoading[processingBank.name]"
      @submit="consentBank(processingBank)"
    />
    <WRejectConsentsDialog
      v-if="processingBank"
      v-model:open="showRejectConsentsAlertDialog"
      :loading="mapBanksToLoading[processingBank.name]"
      @submit="rejectConsent(processingBank)"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import { storeToRefs } from 'pinia'

import { Button as UiButton } from '@/components/ui/button'

import WAccountConsentsDialog from '@/components/widgets/AccountConsentsDialog.vue'
import WRejectConsentsDialog from '@/components/widgets/RejectConsentsDialog.vue'

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

const processingBank = ref<TBank>()
const showAccountConsentsDialog = ref(false)
const showRejectConsentsAlertDialog = ref(false)
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

    toast.success('Банк успешно добавлен')
  } catch (error) {
    if (error instanceof ResponseError) {
      const errorData = await (error as ResponseError).response.json()

      if (errorData.detail === 'Already exists. Already exists.') {
        return toast.error('Банк уже добавлен')
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

    processingBank.value = undefined
    showAccountConsentsDialog.value = false

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

    processingBank.value = undefined
    showRejectConsentsAlertDialog.value = false

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

const openAccountConsentsDialog = (bank: TBank) => {
  processingBank.value = bank
  showAccountConsentsDialog.value = true
}

const openRejectConsentsAlertDialog = (bank: TBank) => {
  processingBank.value = bank
  showRejectConsentsAlertDialog.value = true
}

const getBankButtonText = (name: TBankName) => {
  if (mapBanksToLoading[name]) {
    return 'Загрузка...'
  }

  if (isBankAdded(name)) {
    return isBankConsented(name) ? 'Отозвать согласие' : 'Согласие на подключение'
  }

  return 'Добавить'
}

const getBankButtonDisabled = (name: TBankName) => {
  return mapBanksToLoading[name] || isGetBanksLoading.value
}

const getBankButtonClick = (name: TBankName) => {
  if (isBankAdded(name)) {
    return isBankConsented(name)
      ? openRejectConsentsAlertDialog
      : openAccountConsentsDialog
  }

  return addBank
}

onMounted(getBanks)
</script>