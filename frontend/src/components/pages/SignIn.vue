<template>
  <PAuthCard
    title="Вход в систему"
    description="Введите ваш email и пароль для входа в систему"
  >
    <template #content>
      <FormSignIn />
    </template>
    <template #footer>
      <RouterLink :to="{ name: AuthRouteNames.FORGOT_PASSWORD }" class="text-sm underline text-gray-500 hover:text-gray-700">
        Забыли пароль?
      </RouterLink>
    </template>
  </PAuthCard>
</template>

<script setup lang="ts">
import FormSignIn from '@/components/forms/SignIn.vue'
import PAuthCard from '@/components/partials/AuthCard.vue'

import { AuthRouteNames } from '@/shared/enums'

defineOptions({
  name: 'PageSignIn',
})
</script>
