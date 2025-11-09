<template>
  <div class="flex flex-col gap-4">
    <WRecommendations />
    <UiSeparator />
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <WDebitsAndReceipts />
      <WTransactionsCategories class="col-span-2" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

import WRecommendations from '@/components/widgets/Recommendations.vue'
import WDebitsAndReceipts from '@/components/widgets/DebitsAndReceipts.vue'
import WTransactionsCategories from '@/components/widgets/TransactionsCategories.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

import { useBanksStore } from '@/stores/banks'

defineOptions({
  name: 'PageDashboard',
})

const banksStore = useBanksStore()

onMounted(() => {
  banksStore.getBanks()
})
</script>
