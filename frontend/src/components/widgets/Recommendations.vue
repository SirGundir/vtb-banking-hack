<template>
  <div class="bg-background rounded-lg p-4">
    <div class="flex flex-wrap gap-2">
      <div
        v-for="(recommendation, recommendationIndex) in recommendations"
        :key="`recommendation-${recommendationIndex}`"
        class="bg-background rounded-lg p-4 shadow-sm"
      >
        <component :is="recommendation.icon" class="size-8 mb-4" />
        <h3 class="text-sm font-medium">{{ recommendation.title }}</h3>
        <p class="text-sm text-muted-foreground">{{ recommendation.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Wallet, WalletCards, type LucideIcon } from 'lucide-vue-next'

defineOptions({
  name: 'WidgetRecommendations',
})

interface IRecommendation {
  icon: LucideIcon
  title: string
  description: string
}

const recommendations: IRecommendation[] = [
  {
    icon: Wallet,
    title: 'Вклады',
    description: 'Не упустите выгодное предложение у VTB Банка по вкладам',
  },
  {
    icon: WalletCards,
    title: 'Кредиты',
    description: 'Выгодные условия для рефинансирования кредитов у VTB Банка',
  },
]
</script>
