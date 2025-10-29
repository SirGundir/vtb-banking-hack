import { createRouter, createWebHistory } from 'vue-router'

import { HomeRoute } from '@/router/routes/home'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    HomeRoute,
  ],
})

export default router
