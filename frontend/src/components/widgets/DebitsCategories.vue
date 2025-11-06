<template>
  <div class="bg-background rounded-lg p-4 shadow-sm flex flex-col gap-4">
    <h3>Статистика списаний по категориям</h3>
    <UiSeparator />
    <PDateFilter />
    <PStackedBarChart class="h-[452px]" />
  </div>
</template>

<script setup lang="ts">
import PDateFilter from '@/components/partials/DateFilter.vue'
import PStackedBarChart from '@/components/partials/StackedBarChart.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

defineOptions({
  name: 'WDebitsCategories',
})
</script>
