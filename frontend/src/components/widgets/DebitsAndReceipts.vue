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
import { random } from 'radash'

import { ETransactionType } from '@/shared/enums'

import PTransactionsSelect from '@/components/partials/TransactionsSelect.vue'
import PDateFilter from '@/components/partials/DateFilter.vue'
import PPieChart from '@/components/partials/PieChart.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

import { useMyTransactions } from '@/composables/useMyTransactions'
import { useConnectedBanks } from '@/composables/useConnectedBanks'

defineOptions({
  name: 'WDebitsAndReceipts',
})

const { connectedBanks } = useConnectedBanks()
const { startDate, endDate } = useMyTransactions()
const selectedTransactionType = ref<ETransactionType>(ETransactionType.EXPENSES)

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