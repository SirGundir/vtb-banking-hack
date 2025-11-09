<template>
  <div class="bg-background rounded-lg p-4 shadow-sm flex flex-col gap-4">
    <h3>Статистика по списаниям и поступлениям</h3>
    <UiSeparator />
    <PTransactionsSelect v-model="selectedTransactionType" />
    <PDateFilter v-model:start="startDate" v-model:end="endDate" />
    <PPieChart class="h-[400px]" :data="chartData" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { random } from 'radash'

import { ETransactionType } from '@/shared/enums'
import { AVAILABLE_BANKS } from '@/shared/constants'

import PTransactionsSelect from '@/components/partials/TransactionsSelect.vue'
import PDateFilter from '@/components/partials/DateFilter.vue'
import PPieChart from '@/components/partials/PieChart.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

import { useUserStore } from '@/stores/user'
import { useBanksStore } from '@/stores/banks'

import { useMyTransactions } from '@/composables/useMyTransactions'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const banksStore = useBanksStore()
const { banks } = storeToRefs(banksStore)

defineOptions({
  name: 'WDebitsAndReceipts',
})

const { startDate, endDate } = useMyTransactions()
const selectedTransactionType = ref<ETransactionType>(ETransactionType.EXPENSES)

const connectedBanks = computed(() => {
  return AVAILABLE_BANKS.filter(availableBank => {
    return (banks.value ?? [])
      .filter(bank => user.value?.connectedBanks.includes(bank.id))
      .some(bank => bank.name === availableBank.name)
  })
})

const chartData = computed(() => {
  return {
    labels: connectedBanks.value.map(availableBank => availableBank.name),
    datasets: [
      {
        backgroundColor: connectedBanks.value.map(availableBank => availableBank.brandColor),
        data: connectedBanks.value.map(() => random(0, 100))
      },
    ],
  }
})
</script>