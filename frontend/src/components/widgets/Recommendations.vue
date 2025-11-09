<template>
  <div v-if="isGetRecommendationsLoading" class="flex flex-wrap gap-2">
    <UiSkeleton v-for="i in 3" :key="`skeleton-${i}`" class="w-[280px] h-[100px] rounded-lg" />
  </div>
  <div v-else class="flex flex-wrap gap-2">
    <div
      v-for="(recommendation, recommendationIndex) in recommendations"
      :key="`recommendation-${recommendationIndex}`"
      class="flex flex-col gap-2 rounded-lg p-4 shadow-sm w-[280px] max-w-full"
    >
      <div class="flex items-center gap-2 mb-2">
        <component :is="mapIconsToProductType[recommendation.productType] ?? PackageSearch" class="size-8" />
        <span class="text-sm font-medium">{{ recommendation.bank }}</span>
      </div>
      <h3 class="font-medium">{{ recommendation.productName }}</h3>
      <p class="text-sm text-muted-foreground">{{ recommendation.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { Wallet, WalletCards, CreditCard, PackageSearch, type LucideIcon } from 'lucide-vue-next'

import { useRecommendationsStore } from '@/stores/recommendations'
import { type ProductRecommendation } from '@/api/models/ProductRecommendation'

import { Skeleton as UiSkeleton } from '@/components/ui/skeleton'

const recommendationsStore = useRecommendationsStore()
const { recommendations, isGetRecommendationsLoading } = storeToRefs(recommendationsStore)

defineOptions({
  name: 'WRecommendations',
})

const mapIconsToProductType: Record<ProductRecommendation['productType'], LucideIcon> = {
  'deposit': Wallet,
  'loan': WalletCards,
  'card': CreditCard,
}

onMounted(recommendationsStore.getRecommendations)
</script>
