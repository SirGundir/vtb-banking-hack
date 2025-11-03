<template>
  <UiSidebar collapsible="icon">
    <UiSidebarContent>
      <UiSidebarGroup>
        <UiSidebarMenu>
          <UiSidebarMenuItem>
            <UiSidebarMenuButton
              v-for="link in links"
              :key="link.name"
              as-child
            >
              <RouterLink :to="{ name: link.name }" class="flex items-center gap-2">
                <component :is="link.icon" class="size-4" />
                <span>{{ link.label }}</span>
              </RouterLink>
            </UiSidebarMenuButton>
          </UiSidebarMenuItem>
        </UiSidebarMenu>
      </UiSidebarGroup>
    </UiSidebarContent>
  </UiSidebar>
</template>

<script setup lang="ts">
import { LayoutDashboard, type LucideIcon } from 'lucide-vue-next'
import {
  Sidebar as UiSidebar,
  SidebarContent as UiSidebarContent,
  SidebarGroup as UiSidebarGroup,
  SidebarMenu as UiSidebarMenu,
  SidebarMenuItem as UiSidebarMenuItem,
  SidebarMenuButton as UiSidebarMenuButton,
} from '@/components/ui/sidebar'

import { DashboardRouteNames } from '@/router/routes/dashboard'

defineOptions({
  name: 'WidgetSidebar',
})

interface ISidebarLink {
  label: string
  name: string
  icon: LucideIcon
}

const links: ISidebarLink[] = [
  {
    label: 'Dashboard',
    name: DashboardRouteNames.DASHBOARD,
    icon: LayoutDashboard,
  },

]
</script>