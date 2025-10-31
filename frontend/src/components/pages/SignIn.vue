<template>
  <div class="px-4 flex flex-col items-center justify-start h-screen pt-4 md:pt-20 lg:pt-40">
    <div class="w-[400px] flex flex-col gap-4">
      <WidgetSignTabs />
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>
            Вход в систему
          </UiCardTitle>
          <UiCardDescription>
            Введите ваш email и пароль для входа в систему
          </UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <FormSignIn />
        </UiCardContent>
        <UiCardFooter>
          <RouterLink to="/forgot-password" class="text-sm underline text-gray-500 hover:text-gray-700">
            Забыли пароль?
          </RouterLink>
        </UiCardFooter>
      </UiCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import FormSignIn from '@/components/forms/SignIn.vue'

import UiCard from '@/components/ui/card/Card.vue'
import UiCardHeader from '@/components/ui/card/CardHeader.vue'
import UiCardTitle from '@/components/ui/card/CardTitle.vue'
import UiCardDescription from '@/components/ui/card/CardDescription.vue'
import UiCardContent from '@/components/ui/card/CardContent.vue'
import UiCardFooter from '@/components/ui/card/CardFooter.vue'

import WidgetSignTabs from '@/components/widgets/SignTabs.vue'

defineOptions({
  name: 'PageSignIn',
})
</script>
