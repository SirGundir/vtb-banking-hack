<template>
  <UiTooltipProvider>
    <UiSidebarProvider>
      <div class="__app min-h-screen w-full">
        <RouterView />
        <UiSonner richColors />
      </div>
    </UiSidebarProvider>
  </UiTooltipProvider>
</template>

<script setup lang="ts">
import { provide } from 'vue'

import { TooltipProvider as UiTooltipProvider } from '@/components/ui/tooltip'
import { SidebarProvider as UiSidebarProvider } from '@/components/ui/sidebar'
import { useResize } from '@/composables/useResize'
import { Toaster as UiSonner } from '@/components/ui/sonner'
import 'vue-sonner/style.css'

const { vh } = useResize()

provide('vh', vh)
</script>

<style lang="postcss">
.__app {
  min-height: calc(var(--vh, 1vh) * 100);
}
</style>