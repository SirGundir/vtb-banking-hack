<template>
  <div class="flex flex-wrap items-center justify-between gap-4">
    <UiLabel class="whitespace-nowrap">Период:</UiLabel>
    <UiDateRangePicker />
  </div>
</template>

<script setup lang="ts">
import { Label as UiLabel } from '@/components/ui/label'
import { DateRangePicker as UiDateRangePicker } from '@/components/ui/date-range-picker'

defineOptions({
  name: 'PDateFilter',
})
</script>
