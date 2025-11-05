<template>
  <div class="px-4 pb-4 flex flex-col items-center justify-start h-screen pt-4 md:pt-20 lg:pt-40">
    <div class="w-[450px] max-w-full flex flex-col gap-4">
      <WidgetSignTabs />
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import WidgetSignTabs from '@/components/widgets/SignTabs.vue'

defineOptions({
  name: 'LayoutAuth',
})
</script>
