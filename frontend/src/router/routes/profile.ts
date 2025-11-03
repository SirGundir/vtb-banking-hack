import type { RouteRecordRaw } from 'vue-router'

import PageProfile from '@/components/pages/Profile.vue'

export enum ProfileRouteNames {
  PROFILE = 'Profile',
}

export const ProfileRoute: RouteRecordRaw = {
  name: ProfileRouteNames.PROFILE,
  component: PageProfile,
  path: '/profile',
  meta: {
    auth: true,
  },
}
