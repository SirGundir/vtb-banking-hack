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
    <VeeField
      v-slot="{ componentField, errorMessage, setErrors }"
      :validate-on-blur="true"
      :validate-on-change="false"
      :validate-on-input="false"
      :validate-on-model-update="false"
      name="password"
    >
      <UiFormItem class="relative pb-6 flex flex-col gap-2">
        <UiFormLabel
          required
          :error="!!errorMessage"
        >
          Password
        </UiFormLabel>
        <UiFormControl>
          <UiInput
            v-bind="componentField"
            placeholder="Password"
            :error="!!errorMessage"
            clearable
            type="password"
            autocomplete="current-password"
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
      {{ loading ? 'Входим в систему...' : 'Войти в систему' }}
    </UiButton>
  </VeeForm>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { toTypedSchema } from '@vee-validate/zod'
import { object, string, email, type ZodType } from 'zod'
import {
  Form as VeeForm,
  Field as VeeField,
} from 'vee-validate'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

import {
  FormItem as UiFormItem,
  FormLabel as UiFormLabel,
  FormControl as UiFormControl,
  FormMessage as UiFormMessage,
} from '@/components/ui/form'
import { Input as UiInput } from '@/components/ui/input'
import { Button as UiButton } from '@/components/ui/button'

import { type LoginDTO } from '@/api/models/LoginDTO'
import { MeRouteNames } from '@/router/routes/me'
import { useUserStore } from '@/stores/user'
import { ResponseError } from '@/api/runtime'

const { signIn } = useUserStore()
const router = useRouter()

defineOptions({
  name: 'FormSignIn',
})

const formSchema = toTypedSchema(object({
  email: email({ message: 'Invalid email address' }),
  password: string().min(8),
}) satisfies ZodType<LoginDTO>)

const initialValues: LoginDTO = {
  email: 'test@test.com',
  password: 'Qwerty123!',
}

const loading = ref(false)

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const handleSubmit = async (values: any) => {
  const submittedForm = values as typeof initialValues

  try {
    loading.value = true

    await signIn(submittedForm)
    router.push({ name: MeRouteNames.DASHBOARD })
  } catch (error: unknown) {
    if (error instanceof ResponseError && error.response.status === 404) {
      return toast.error('Такого пользователя не существует')
    }
    if (error instanceof ResponseError && error.response.status === 401) {
      return toast.error('Неверный логин или пароль')
    }
    if (error instanceof ResponseError && error.response.status === 500) {
      return toast.error('Ошибка сервера')
    }
    
    toast.error('Неизвестная ошибка')
  } finally {
    loading.value = false
  }
}
</script>
