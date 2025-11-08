<template>
  <div class="flex flex-wrap gap-2">
    <div
      v-for="(recommendation, recommendationIndex) in recommendations"
      :key="`recommendation-${recommendationIndex}`"
      class="bg-background rounded-lg p-4 shadow-sm w-[280px] max-w-full"
    >
      <component :is="recommendation.icon" class="size-8 mb-4" />
      <h3 class="text-sm font-medium">{{ recommendation.title }}</h3>
      <p class="text-sm text-muted-foreground">{{ recommendation.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Wallet, WalletCards, type LucideIcon } from 'lucide-vue-next'

defineOptions({
  name: 'WRecommendations',
})

interface IRecommendation {
  icon: LucideIcon
  title: string
  description: string
}

const recommendations: IRecommendation[] = [
  {
    icon: Wallet,
    title: 'Вклад с наименьшим процентом',
    description: 'Не упустите выгодное предложение у VTB Банка по вкладам',
  },
  {
    icon: WalletCards,
    title: 'Очень выгодный кредит',
    description: 'Выгодные условия для рефинансирования кредитов у VTB Банка',
  },
]
</script>
