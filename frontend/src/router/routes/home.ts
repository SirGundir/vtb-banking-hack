import type { RouteRecordRaw } from 'vue-router'

import PageHome from '@/components/pages/Home.vue'

export enum HomeRouteNames {
  HOME = 'Home',
}

export const HomeRoute: RouteRecordRaw = {
  name: HomeRouteNames.HOME,
  component: PageHome,
  path: '/',
  meta: {
    auth: true,
  },
}
