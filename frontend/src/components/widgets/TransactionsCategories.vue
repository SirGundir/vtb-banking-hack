<template>
  <div class="bg-background rounded-lg p-4 shadow-sm flex flex-col gap-4">
    <h3>Статистика транзакций по категориям</h3>
    <UiSeparator />
    <PDateFilter v-model:start="startDate" v-model:end="endDate" />
    <PStackedBarChart :data="chartData" class="h-[452px]" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import PDateFilter from '@/components/partials/DateFilter.vue'
import PStackedBarChart from '@/components/partials/StackedBarChart.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

import { useMyTransactions } from '@/composables/useMyTransactions'

const { transactions, startDate, endDate } = useMyTransactions()

defineOptions({
  name: 'WTransactionsCategories',
})

const categories = computed(() => {
  return Array.from(new Set(transactions.value.map(transaction => transaction.transactionInfo)))
})

const chartData = computed(() => {
  return {
    labels: categories.value,
    datasets: [
      {
        label: 'Транзакции',
        data: categories.value.map(category => transactions.value.filter(transaction => transaction.transactionInfo === category).map(transaction => transaction.amount).reduce((acc, curr) => acc + curr, 0)),
        backgroundColor: '#40b983',
      }
    ],
  }
})
</script>
