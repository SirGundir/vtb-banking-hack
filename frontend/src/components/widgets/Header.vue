<template>
  <div class="flex gap-4 items-center justify-between pl-2 pr-4 py-2 bg-background dark:bg-black border-b border-border">
    <div class="flex items-center gap-2 ml-0.5 h-7">
      <UiSidebarTrigger v-if="!hideSidebar" />
      <UiSeparator v-if="!hideSidebar" orientation="vertical" />
      <PLogo :class="hideSidebar ? 'ml-1.5' : ''" />
    </div>
    <PUserMenu />
  </div>
</template>

<script setup lang="ts">
import { SidebarTrigger as UiSidebarTrigger } from '@/components/ui/sidebar'
import { Separator as UiSeparator } from '@/components/ui/separator'

import PUserMenu from '@/components/partials/UserMenu.vue'
import PLogo from '@/components/partials/Logo.vue'

defineOptions({
  name: 'WHeader',
})

const {
  hideSidebar = false,
} = defineProps<{
  hideSidebar?: boolean
}>()
</script>
