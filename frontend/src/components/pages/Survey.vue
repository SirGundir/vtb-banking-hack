<template>
  <div class="flex flex-col items-start gap-4">
    <div class="flex flex-col mb-4">
      <h1 class="text-xl font-medium mb-2">Настройка целей</h1>
      <p class="text-sm text-muted-foreground">Выберите цели, которые вы хотите достичь, чтобы мы могли предоставить вам наиболее точные рекомендации</p>
    </div>
    <WSurvey />
    <RouterLink v-if="hasConnectedBanks" :to="{ name: OnboardingRouteNames.BANKS }">
      <UiButton variant="outline" size="sm" class="w-fit">
        <ArrowLeft class="size-4" />
        Вернуться к подключению банков
      </UiButton>
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'

import WSurvey from '@/components/widgets/Survey.vue'

import { Button as UiButton } from '@/components/ui/button'

import { useUserStore } from '@/stores/user'

import { OnboardingRouteNames } from '@/shared/enums'

const userStore = useUserStore()
const { hasConnectedBanks } = storeToRefs(userStore)

defineOptions({
  name: 'PageSurvey',
})
</script>
