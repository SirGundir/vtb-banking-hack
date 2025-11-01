<template>
  <LayoutAuth>
    <UiCard>
      <UiCardHeader>
        <UiCardTitle>
          Забыли пароль?
        </UiCardTitle>
        <UiCardDescription>
          Введите ваш email для получения ссылки на восстановление пароля
        </UiCardDescription>
      </UiCardHeader>
      <UiCardContent>
        <FormForgotPassword />
      </UiCardContent>
    </UiCard>
  </LayoutAuth>
</template>

<script setup lang="ts">
import LayoutAuth from '@/components/layouts/Auth.vue'

import UiCard from '@/components/ui/card/Card.vue'
import UiCardHeader from '@/components/ui/card/CardHeader.vue'
import UiCardTitle from '@/components/ui/card/CardTitle.vue'
import UiCardDescription from '@/components/ui/card/CardDescription.vue'
import UiCardContent from '@/components/ui/card/CardContent.vue'

import FormForgotPassword from '@/components/forms/ForgotPassword.vue'

defineOptions({
  name: 'PageForgotPassword',
})
</script>
