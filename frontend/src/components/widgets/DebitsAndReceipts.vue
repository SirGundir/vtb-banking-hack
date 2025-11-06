<template>
  <div class="bg-background rounded-lg p-4 shadow-sm flex flex-col gap-4">
    <h3>Статистика по списаниям и поступлениям</h3>
    <UiSeparator />
    <PTransactionsSelect v-model="selectedTransactionType" />
    <PDateFilter />
    <PPieChart class="h-[400px]" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { ETransactionType } from '@/shared/enums'

import PTransactionsSelect from '@/components/partials/TransactionsSelect.vue'
import PDateFilter from '@/components/partials/DateFilter.vue'
import PPieChart from '@/components/partials/PieChart.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

defineOptions({
  name: 'WDebitsAndReceipts',
})

const selectedTransactionType = ref<ETransactionType>(ETransactionType.EXPENSES)
</script>