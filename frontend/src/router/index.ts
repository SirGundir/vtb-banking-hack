import { createRouter, createWebHashHistory } from 'vue-router'

import {
  MeRoute,
  MeRouteNames,
} from '@/router/routes/me'
import {
  AuthRoute,
  AuthRouteNames,
} from '@/router/routes/auth'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: { name: MeRouteNames.ME },
    },
    MeRoute,
    AuthRoute,
  ],
})

router.beforeEach(async (to, from, next) => {
  if (!to.meta.auth) return next()

  const userStore = useUserStore()

  if (!userStore.user) {
    try {
      await userStore.getMe()
    } catch (error: unknown) {
      console.error(error)
      return next({ name: AuthRouteNames.SIGN_IN })
    }
  }

  return next()
})

export default router
