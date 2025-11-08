import type { RouteRecordRaw } from 'vue-router'

import LayoutMe from '@/components/layouts/Me.vue'

import PageProfileMain from '@/components/pages/ProfileMain.vue'

import { ProfileRouteNames } from '@/shared/enums'

export const ProfileMainRoute: RouteRecordRaw = {
  name: ProfileRouteNames.MAIN,
  component: PageProfileMain,
  path: 'main',
}

export const ProfileRoute: RouteRecordRaw = {
  name: ProfileRouteNames.PROFILE,
  path: '/profile',
  component: LayoutMe,
  redirect: { name: ProfileRouteNames.MAIN },
  children: [
    ProfileMainRoute,
  ],
  meta: {
    auth: true,
  },
}