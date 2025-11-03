<template>
  <div class="flex gap-4 items-center justify-between pl-2 pr-4 py-2 bg-background dark:bg-black shadow-sm">
    <div class="flex items-center gap-2 ml-0.5 h-7">
      <UiSidebarTrigger />
      <UiSeparator orientation="vertical" />
      <div class="text-lg font-medium">OneBank</div>
    </div>
    <PartialUserMenu />
  </div>
</template>

<script setup lang="ts">
import { SidebarTrigger as UiSidebarTrigger } from '@/components/ui/sidebar'
import { Separator as UiSeparator } from '@/components/ui/separator'
import PartialUserMenu from '@/components/partials/UserMenu.vue'

defineOptions({
  name: 'WidgetHeader',
})
</script>
