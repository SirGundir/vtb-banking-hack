import type { RouteRecordRaw } from 'vue-router'

import HomePage from '@/components/pages/Home.vue'

export const HomeRoute: RouteRecordRaw = {
  component: HomePage,
  path: '/',
}
