<template>
  <PAuthCard
    title="Забыли пароль?"
    description="Введите ваш email для получения ссылки на восстановление пароля"
  >
    <template #content>
      <FormForgotPassword />
    </template>
  </PAuthCard>
</template>

<script setup lang="ts">
import FormForgotPassword from '@/components/forms/ForgotPassword.vue'
import PAuthCard from '@/components/partials/AuthCard.vue'

defineOptions({
  name: 'PageForgotPassword',
})
</script>
