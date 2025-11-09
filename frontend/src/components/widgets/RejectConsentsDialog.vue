<template>
  <UiDialog v-model:open="isOpen">
    <UiDialogContent class="sm:max-w-md">
      <UiDialogHeader>
        <UiDialogTitle>Отмена согласия</UiDialogTitle>
        <UiDialogDescription>
          Вы уверены, что хотите отменить согласие на доступ к счетам?
        </UiDialogDescription>
      </UiDialogHeader>
      <UiSeparator />
      <UiDialogFooter class="sm:justify-end">
        <UiButton
          variant="outline"
          type="button"
          :disabled="loading"
          @click="$emit('submit')"
        >
          {{ loading ? 'Загрузка...' : 'Отменить согласие' }}
        </UiButton>
        <UiDialogClose as-child>
          <UiButton type="button">
            Закрыть
          </UiButton>
        </UiDialogClose>
      </UiDialogFooter>
    </UiDialogContent>
  </UiDialog>
</template>

<script setup lang="ts">
import { useVModel } from '@vueuse/core'

import {
  Dialog as UiDialog,
  DialogContent as UiDialogContent,
  DialogHeader as UiDialogHeader,
  DialogTitle as UiDialogTitle,
  DialogDescription as UiDialogDescription,
  DialogFooter as UiDialogFooter,
  DialogClose as UiDialogClose,
} from '@/components/ui/dialog'
import { Button as UiButton } from '@/components/ui/button'
import { Separator as UiSeparator } from '@/components/ui/separator'

defineOptions({
  name: 'WRejectConsentsDialog',
})

const props = defineProps<{
  open: boolean
  loading: boolean
}>()

const emits = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'submit'): void
}>()

const isOpen = useVModel(props, 'open', emits)
</script>