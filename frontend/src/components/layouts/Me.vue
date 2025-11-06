<template>
  <div class="flex">
    <WSidebar />
    <div class="flex grow flex-col min-h-screen">
      <WHeader />
      <WRecommendations />
      <UiSeparator />
      <div class="flex-1 p-4">
        <RouterView />
      </div>
      <WFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import WSidebar from '@/components/widgets/Sidebar.vue'
import WHeader from '@/components/widgets/Header.vue'
import WRecommendations from '@/components/widgets/Recommendations.vue'
import WFooter from '@/components/widgets/Footer.vue'

import { Separator as UiSeparator } from '@/components/ui/separator'

defineOptions({
  name: 'LayoutMe',
})
</script>
