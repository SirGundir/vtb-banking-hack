<template>
  <div class="flex flex-wrap items-center justify-between gap-4">
    <UiLabel class="whitespace-nowrap">Период:</UiLabel>
    <UiDateRangePicker v-model:start="start" v-model:end="end"/>
  </div>
</template>

<script setup lang="ts">
import { useVModel } from '@vueuse/core'

import { Label as UiLabel } from '@/components/ui/label'
import { DateRangePicker as UiDateRangePicker } from '@/components/ui/date-range-picker'

defineOptions({
  name: 'PDateFilter',
})

const props = defineProps<{
  start?: Date
  end?: Date
}>()

const emits = defineEmits<{
  (event: 'update:start', value?: Date): void
  (event: 'update:end', value?: Date): void
}>()

const start = useVModel(props, 'start', emits)
const end = useVModel(props, 'end', emits)
</script>
