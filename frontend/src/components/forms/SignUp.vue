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
    <VeeField
      v-slot="{ componentField, errorMessage, setErrors }"
      :validate-on-blur="true"
      :validate-on-change="false"
      :validate-on-input="false"
      :validate-on-model-update="false"
      name="firstName"
    >
      <UiFormItem class="relative pb-6 flex flex-col gap-2">
        <UiFormLabel
          :error="!!errorMessage"
        >
          Имя
        </UiFormLabel>
        <UiFormControl>
          <UiInput
            v-bind="componentField"
            placeholder="Введите ваше имя"
            :error="!!errorMessage"
            clearable
            type="text"
            autocomplete="given-name"
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
      name="lastName"
    >
      <UiFormItem class="relative pb-6 flex flex-col gap-2">
        <UiFormLabel
          :error="!!errorMessage"
        >
          Фамилия
        </UiFormLabel>
        <UiFormControl>
          <UiInput
            v-bind="componentField"
            placeholder="Введите вашу фамилию"
            :error="!!errorMessage"
            clearable
            type="text"
            autocomplete="family-name"
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
    <div class="flex items-center gap-2 mb-6">
      <UiCheckbox v-model="isAgreed" id="terms" class="cursor-pointer" />
      <UiLabel
        for="terms"
        class="cursor-pointer"
      >
        Я согласен на обработку персональных данных
      </UiLabel>
    </div>
    <UiButton
      type="submit"
      class="w-full"
      size="lg"
      :disabled="loading || !isAgreed"
    >
      {{ loading ? 'Регистрируемся...' : 'Регистрация' }}
    </UiButton>
  </VeeForm>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { toTypedSchema } from '@vee-validate/zod'
import { object, string, email, type ZodType } from 'zod'

import { Form as VeeForm, Field as VeeField } from 'vee-validate'

import UiFormItem from '@/components/ui/form/FormItem.vue'
import UiFormLabel from '@/components/ui/form/FormLabel.vue'
import UiFormControl from '@/components/ui/form/FormControl.vue'
import UiFormMessage from '@/components/ui/form/FormMessage.vue'
import UiInput from '@/components/ui/input/Input.vue'
import UiButton from '@/components/ui/button/Button.vue'
import UiLabel from '@/components/ui/label/Label.vue'
import UiCheckbox from '@/components/ui/checkbox/Checkbox.vue'

import { type CreateUserDTO } from '@/api/models/CreateUserDTO'
import { MeRouteNames } from '@/router/routes/me'
import { useUserStore } from '@/stores/user'

const { signUp } = useUserStore()
const router = useRouter()

defineOptions({
  name: 'FormSignUp',
})

const formSchema = toTypedSchema(object({
  email: email({ message: 'Invalid email address' }),
  password: string().min(8),
  firstName: string().min(1).max(255).optional(),
  lastName: string().min(1).max(255).optional(),
}) satisfies ZodType<CreateUserDTO>)

const initialValues: CreateUserDTO = {
  email: 'test@test.com',
  password: 'Qwerty123!',
  firstName: 'John',
  lastName: 'Doe',
  language: 'ru',
}

const isAgreed = ref(false)
const loading = ref(false)

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const handleSubmit = async (values: any) => {
  const submittedForm = values as typeof initialValues

  try {
    loading.value = true

    await signUp(submittedForm)
    router.push({ name: MeRouteNames.DASHBOARD })
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>