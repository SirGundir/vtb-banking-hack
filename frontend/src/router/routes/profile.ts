import type { RouteRecordRaw } from 'vue-router'

import LayoutProfile from '@/components/layouts/Profile.vue'

import PageProfileMain from '@/components/pages/ProfileMain.vue'

export enum ProfileRouteNames {
  PROFILE = 'Profile',
  MAIN = 'Main',
}

export const ProfileMainRoute: RouteRecordRaw = {
  name: ProfileRouteNames.MAIN,
  component: PageProfileMain,
  path: 'main',
}

export const ProfileRoute: RouteRecordRaw = {
  name: ProfileRouteNames.PROFILE,
  path: '/profile',
  component: LayoutProfile,
  redirect: { name: ProfileRouteNames.MAIN },
  children: [
    ProfileMainRoute,
  ],
  meta: {
    auth: true,
  },
}