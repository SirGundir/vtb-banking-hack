<template>
  <UiDialog v-model:open="isOpen">
    <UiDialogContent class="sm:max-w-md">
      <UiDialogHeader>
        <UiDialogTitle>Согласие на доступ к счетам</UiDialogTitle>
        <UiDialogDescription>
          Для того чтобы мы могли предоставить вам наиболее точные рекомендации, нам необходимо получить доступ к информации по вашим счетам.
        </UiDialogDescription>
      </UiDialogHeader>
      <UiSeparator />
      <div class="flex flex-col gap-4">
        <p class="text-sm">Вы даёте свое согласие приложению «OneBank»<br />на обработку ваших персональных данных и получение информации о ваших счетах, балансах и транзакциях из банка <span class="font-medium">"{{ bankName }}"</span> в соответствии со ст. 9 Ф3 Nº152 «О персональных данных» и стандартами Банка России (СТО БР ФАПИ. СЕК-1.6-2024).<br /><br />Вы даёте своё согласие приложению "OneBank"<br />на обработку ваших персональных данных и получение информации о ваших счетах.</p>

        <UiSeparator />

        <div class="flex flex-col gap-2">
          <div
            v-for="(consent, consentKey) in consents"
            :key="consentKey"
            class="flex items-center gap-2"
          >
            <UiCheckbox v-model="consent.value" :id="`consent-${consentKey}`" />
            <UiLabel :for="`consent-${consentKey}`">{{ consent.label }}</UiLabel>
          </div>
        </div>
      </div>
      <UiSeparator />
      <UiDialogFooter class="sm:justify-end">
        <UiDialogClose as-child>
          <UiButton type="button" variant="secondary">
            Закрыть
          </UiButton>
        </UiDialogClose>
        <UiButton
          type="button"
          :disabled="isDisabledSubmit || loading"
          @click="$emit('submit')"
        >
          {{ loading ? 'Загрузка...' : 'Отправить' }}
        </UiButton>
      </UiDialogFooter>
    </UiDialogContent>
  </UiDialog>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
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
import { Checkbox as UiCheckbox } from '@/components/ui/checkbox'
import { Label as UiLabel } from '@/components/ui/label'
import { Separator as UiSeparator } from '@/components/ui/separator'

defineOptions({
  name: 'WAccountConsentsDialog',
})

const props = defineProps<{
  open: boolean
  loading: boolean
  bankName: string
}>()

const emits = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'submit'): void
}>()

const isOpen = useVModel(props, 'open', emits)

enum EConsent {
  PERSONAL = 'personal',
  ACCOUNTS = 'accounts',
  POLICY = 'policy',
}

type TConsent = `${EConsent}`

interface IConsent {
  value: boolean
  label: string
}

const consents = reactive<Record<TConsent, IConsent>>({
  personal: {
    value: false,
    label: 'Я соглашаюсь на обработку персональных данных.'
  },
  accounts: {
    value: false,
    label: 'Я разрешаю получение данных о моих банковских счетах, балансах и транзакциях.'
  },
  policy: {
    value: false,
    label: 'Я ознакомлен с политикой конфиденциальности.'
  }
})

const isDisabledSubmit = computed(() => {
  return Object.values(consents).some(consent => !consent.value)
})
</script>