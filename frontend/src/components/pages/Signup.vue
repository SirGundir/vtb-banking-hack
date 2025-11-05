<template>
  <UiCard>
    <UiCardHeader>
      <UiCardTitle>
        Регистрация в системе
      </UiCardTitle>
      <UiCardDescription>
        Введите ваши данные для регистрации в системе
      </UiCardDescription>
    </UiCardHeader>
    <UiCardContent>
      <FormSignUp />
    </UiCardContent>
  </UiCard>
</template>

<script setup lang="ts">
import UiCard from '@/components/ui/card/Card.vue'
import UiCardHeader from '@/components/ui/card/CardHeader.vue'
import UiCardTitle from '@/components/ui/card/CardTitle.vue'
import UiCardDescription from '@/components/ui/card/CardDescription.vue'
import UiCardContent from '@/components/ui/card/CardContent.vue'

import FormSignUp from '@/components/forms/SignUp.vue'

defineOptions({
  name: 'PageSignup',
})
</script>
