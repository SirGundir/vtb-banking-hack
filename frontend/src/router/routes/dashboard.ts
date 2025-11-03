import type { RouteRecordRaw } from 'vue-router'

import PageDashboard from '@/components/pages/Dashboard.vue'

export enum DashboardRouteNames {
  DASHBOARD = 'Dashboard',
}

export const DashboardRoute: RouteRecordRaw = {
  name: DashboardRouteNames.DASHBOARD,
  component: PageDashboard,
  path: '/',
  meta: {
    auth: true,
  },
}
