<template>
  <div class="flex items-center justify-between gap-4">
    <UiLabel class="whitespace-nowrap">Тип транзакции:</UiLabel>
    <UiSelect
      v-model="vModelValue"
      :defaultValue="TransactionDirection.Credit"
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

import { TransactionDirection } from '@/api/models/TransactionDirection'

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
  modelValue: TransactionDirection
}>()

const emits = defineEmits<{
  (event: 'update:modelValue', value: TransactionDirection): void
}>()

const vModelValue = useVModel(props, 'modelValue', emits, {
  passive: true,
  defaultValue: TransactionDirection.Credit,
})

const mapTransactionTypeToLabel: Record<TransactionDirection, string> = {
  [TransactionDirection.Credit]: 'Поступление',
  [TransactionDirection.Debit]: 'Списание',
}

const availableTransactionTypes = Object.values(TransactionDirection).map(value => ({
  label: mapTransactionTypeToLabel[value],
  value,
}))
</script>