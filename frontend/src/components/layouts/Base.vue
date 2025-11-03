<template>
  <div class="flex">
    <WidgetSidebar />
    <div class="flex grow flex-col min-h-screen">
      <WidgetHeader />
      <div class="flex-1 p-4">
        <slot />
      </div>
      <WidgetFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import WidgetSidebar from '@/components/widgets/Sidebar.vue'
import WidgetHeader from '@/components/widgets/Header.vue'
import WidgetFooter from '@/components/widgets/Footer.vue'

defineOptions({
  name: 'LayoutBase',
})
</script>
