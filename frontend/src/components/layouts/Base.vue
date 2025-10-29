<template>
  <div class="flex flex-col">
    <WidgetHeader />
    <slot />
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
