<template>
  <div class="flex flex-col min-h-screen">
    <WidgetHeader />
    <div class="flex-1 p-4">
      <slot />
    </div>
    <WidgetFooter />
  </div>
</template>

<script setup lang="ts">
import WidgetHeader from '@/components/widgets/Header.vue'
import WidgetFooter from '@/components/widgets/Footer.vue'

defineOptions({
  name: 'LayoutBase',
})
</script>
