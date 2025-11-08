<template>
  <div class="flex">
    <div class="flex grow flex-col min-h-screen">
      <WHeader hideSidebar />
      <div class="flex-1 p-4">
        <RouterView />
      </div>
      <WFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import WHeader from '@/components/widgets/Header.vue'
import WFooter from '@/components/widgets/Footer.vue'

defineOptions({
  name: 'LayoutProfile',
})
</script>
