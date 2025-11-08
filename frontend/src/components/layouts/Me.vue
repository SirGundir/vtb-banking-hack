<template>
  <div class="flex">
    <WSidebar v-if="hasConnectedBanks" />
    <div class="flex grow flex-col min-h-screen">
      <WHeader :hide-sidebar="!hasConnectedBanks" />
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
import WFooter from '@/components/widgets/Footer.vue'

import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { hasConnectedBanks } = storeToRefs(userStore)

defineOptions({
  name: 'LayoutMe',
})
</script>
