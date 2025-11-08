<template>
  <div class="flex flex-col items-start gap-4">
    <div class="flex flex-col mb-4">
      <h1 class="text-xl font-medium mb-2">Доступные банки</h1>
      <p class="text-sm text-muted-foreground">Выберите банки, которые вы хотите подключить к своему аккаунту</p>
    </div>
    <WAvailableBanks />
    <RouterLink v-if="hasConnectedBanks" :to="{ name: OnboardingRouteNames.SURVEY }">
      <UiButton variant="outline" size="sm" class="w-fit">
        Перейти к настройке целей
        <ArrowRight class="size-4" />
      </UiButton>
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { ArrowRight } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'

import WAvailableBanks from '@/components/widgets/AvailableBanks.vue'

import { Button as UiButton } from '@/components/ui/button'

import { useUserStore } from '@/stores/user'

import { OnboardingRouteNames } from '@/shared/enums'

const userStore = useUserStore()
const { hasConnectedBanks } = storeToRefs(userStore)

defineOptions({
  name: 'PageBanks',
})
</script>
