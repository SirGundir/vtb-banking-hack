<template>
  <UiDialog v-model:open="isOpen">
    <UiDialogContent class="sm:max-w-md">
      <UiDialogHeader>
        <UiDialogTitle>Согласие на доступ к счетам</UiDialogTitle>
        <UiDialogDescription>
          Для того чтобы мы могли предоставить вам наиболее точные рекомендации, нам необходимо получить доступ к информации по вашим счетам.
        </UiDialogDescription>
      </UiDialogHeader>
      <div class="flex flex-col gap-4">
        <p>Вы даёте свое согласие приложению «OneBank»<br />на обработку ваших персональных данных и получение информации о ваших счетах, балансах и транзакциях из выбранного банка в соответствии со ст. 9 Ф3 Nº152 «О персональных данных» и стандартами Банка России (СТО БР ФАПИ. СЕК-1.6-2024).<br />Вы даёте своё согласие приложению "OneBank"<br />на обработку ваших персональных данных и получение информации о ваших счетах.</p>

        <div class="flex flex-col gap-2">
          <div
            v-for="(consent, consentKey) in consents"
            :key="consentKey"
            class="flex items-center gap-2"
          >
            <UiCheckbox v-model="consent.value" />
            <UiLabel :for="consentKey">{{ consent.label }}</UiLabel>
          </div>
        </div>
      </div>
      <UiDialogFooter class="sm:justify-end">
        <UiDialogClose as-child>
          <UiButton type="button" variant="secondary">
            Закрыть
          </UiButton>
          <UiButton type="button" @click="$emit('submit')">
            Отправить
          </UiButton>
        </UiDialogClose>
      </UiDialogFooter>
    </UiDialogContent>
  </UiDialog>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
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

defineOptions({
  name: 'WAccountConsentsDialog',
})

const props = defineProps<{
  open: boolean
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
</script>