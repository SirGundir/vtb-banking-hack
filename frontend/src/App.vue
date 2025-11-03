<template>
  <UiTooltipProvider>
    <UiSidebarProvider>
      <WidgetSidebar />
      <div class="__app min-h-screen w-full">
        <RouterView />
      </div>
    </UiSidebarProvider>
  </UiTooltipProvider>
</template>

<script setup lang="ts">
import { provide } from 'vue'

import WidgetSidebar from '@/components/widgets/Sidebar.vue'
import { TooltipProvider as UiTooltipProvider } from '@/components/ui/tooltip'
import { SidebarProvider as UiSidebarProvider } from '@/components/ui/sidebar'
import { useResize } from '@/composables/useResize'

const { vh } = useResize()

provide('vh', vh)
</script>

<style lang="postcss">
.__app {
  min-height: calc(var(--vh, 1vh) * 100);
}
</style>