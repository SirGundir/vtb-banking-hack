import type { RouteRecordRaw } from 'vue-router'

import LayoutMe from '@/components/layouts/Me.vue'

import PageDashboard from '@/components/pages/Dashboard.vue'

import {
  OnboardingRouteNames,
} from '@/router/routes/onboarding'

import { useUserStore } from '@/stores/user'

export enum MeRouteNames {
  ME = 'Me',
  DASHBOARD = 'Dashboard',
}

export const MeDashboardRoute: RouteRecordRaw = {
  name: MeRouteNames.DASHBOARD,
  component: PageDashboard,
  path: 'dashboard',
  meta: {
    auth: true,
  },
}

export const MeRoute: RouteRecordRaw = {
  name: MeRouteNames.ME,
  path: '/me',
  redirect: { name: MeRouteNames.DASHBOARD },
  component: LayoutMe,
  beforeEnter: async (to, from, next) => {
    const userStore = useUserStore()
    if (!userStore.hasConnectedBanks) {
      return next({ name: OnboardingRouteNames.ONBOARDING })
    }
    next()
  },
  children: [
    MeDashboardRoute,
  ],
}
