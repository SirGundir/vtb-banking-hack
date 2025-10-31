<template>
  <div class="px-4 flex flex-col items-center justify-start h-screen pt-4 md:pt-20 lg:pt-40">
    <div class="w-[400px] flex flex-col gap-4">
      <WidgetSignTabs />
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
          Форма регистрации
        </UiCardContent>
      </UiCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import UiCard from '@/components/ui/card/Card.vue'
import UiCardHeader from '@/components/ui/card/CardHeader.vue'
import UiCardTitle from '@/components/ui/card/CardTitle.vue'
import UiCardDescription from '@/components/ui/card/CardDescription.vue'
import UiCardContent from '@/components/ui/card/CardContent.vue'

import WidgetSignTabs from '@/components/widgets/SignTabs.vue'

defineOptions({
  name: 'PageSignup',
})
</script>
