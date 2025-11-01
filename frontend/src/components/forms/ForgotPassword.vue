<template>
  <VeeForm
    :validation-schema="formSchema"
    :initial-values="initialValues"
    class="flex flex-col"
    @submit="handleSubmit"
  >
    <VeeField
      v-slot="{ componentField, errorMessage, setErrors }"
      :validate-on-blur="true"
      :validate-on-change="false"
      :validate-on-input="false"
      :validate-on-model-update="false"
      name="email"
    >
      <UiFormItem class="relative pb-6 flex flex-col gap-2">
        <UiFormLabel
          required
          :error="!!errorMessage"
        >
          Email
        </UiFormLabel>
        <UiFormControl>
          <UiInput
            v-bind="componentField"
            placeholder="email@example.com"
            :error="!!errorMessage"
            clearable
            type="email"
            autocomplete="username"
            class="bg-white dark:bg-black"
            @focus="setErrors('')"
          />
        </UiFormControl>
        <UiFormMessage
          v-if="errorMessage"
          class="absolute bottom-0 mb-1 left-0 w-full"
        >
          {{ errorMessage }}
        </UiFormMessage>
      </UiFormItem>
    </VeeField>
    <UiButton
      type="submit"
      class="w-full"
      size="lg"
      :disabled="loading"
    >
      {{ loading ? 'Отправляем письмо...' : 'Сбросить пароль' }}
    </UiButton>
  </VeeForm>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { toTypedSchema } from '@vee-validate/zod'
import { object, email, type ZodType } from 'zod'

import {
  Form as VeeForm,
  Field as VeeField,
} from 'vee-validate'

import UiFormItem from '@/components/ui/form/FormItem.vue'
import UiFormLabel from '@/components/ui/form/FormLabel.vue'
import UiFormControl from '@/components/ui/form/FormControl.vue'
import UiFormMessage from '@/components/ui/form/FormMessage.vue'
import UiInput from '@/components/ui/input/Input.vue'
import UiButton from '@/components/ui/button/Button.vue'

import { type ResetPasswordDTO } from '@/api/models/ResetPasswordDTO'
import { useUserStore } from '@/stores/user'

const { resetEmail } = useUserStore()

defineOptions({
  name: 'FormForgotPassword',
})

const formSchema = toTypedSchema(object({
  email: email({ message: 'Invalid email address' }),
}) satisfies ZodType<ResetPasswordDTO>)

const initialValues: ResetPasswordDTO = {
  email: 'test@test.com',
}

const loading = ref(false)

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const handleSubmit = async (values: any) => {
  const submittedForm = values as typeof initialValues

  try {
    loading.value = true

    await resetEmail(submittedForm.email)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
