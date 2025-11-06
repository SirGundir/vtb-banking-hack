<template>
  <div class="flex items-center justify-between gap-4">
    <UiLabel class="whitespace-nowrap">Тип транзакции:</UiLabel>
    <UiSelect
      v-model="vModelValue"
      :defaultValue="ETransactionType.EXPENSES"
    >
      <UiSelectTrigger class="cursor-pointer">
        <UiSelectValue
          placeholder="Выберите тип транзакции"
          :aria-label="vModelValue"
        >
          {{ mapTransactionTypeToLabel[vModelValue] }}
        </UiSelectValue>
      </UiSelectTrigger>
      <UiSelectContent>
        <UiSelectItem
          v-for="type in availableTransactionTypes"
          :key="type.value"
          :value="type.value"
          class="cursor-pointer"
        >
          {{ type.label }}
        </UiSelectItem>
      </UiSelectContent>
    </UiSelect>
  </div>
</template>

<script setup lang="ts">
import { useVModel } from '@vueuse/core'

import { ETransactionType } from '@/shared/enums'

import {
  Select as UiSelect,
  SelectTrigger as UiSelectTrigger,
  SelectValue as UiSelectValue,
  SelectContent as UiSelectContent,
  SelectItem as UiSelectItem,
} from '@/components/ui/select'
import { Label as UiLabel } from '@/components/ui/label'

defineOptions({
  name: 'PTransactionsSelect',
})

const props = defineProps<{
  modelValue: `${ETransactionType}`
}>()

const emits = defineEmits<{
  (event: 'update:modelValue', value: `${ETransactionType}`): void
}>()

const vModelValue = useVModel(props, 'modelValue', emits, {
  passive: true,
  defaultValue: ETransactionType.EXPENSES,
})

const mapTransactionTypeToLabel: Record<`${ETransactionType}`, string> = {
  [ETransactionType.INCOME]: 'Поступление',
  [ETransactionType.EXPENSES]: 'Списание',
}

const availableTransactionTypes = Object.values(ETransactionType).map(value => ({
  label: mapTransactionTypeToLabel[value],
  value,
}))
</script>