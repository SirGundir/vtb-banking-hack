<template>
  <PAuthCard
    title="Регистрация в системе"
    description="Введите ваши данные для регистрации в системе"
  >
    <template #content>
      <FormSignUp />
    </template>
  </PAuthCard>
</template>

<script setup lang="ts">
import FormSignUp from '@/components/forms/SignUp.vue'
import PAuthCard from '@/components/partials/AuthCard.vue'

defineOptions({
  name: 'PageSignup',
})
</script>
