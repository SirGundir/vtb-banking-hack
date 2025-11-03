import { createRouter, createWebHashHistory } from 'vue-router'

import { DashboardRoute } from '@/router/routes/dashboard'
import { SignInRoute, SignupRoute, ForgotPasswordRoute, AuthRouteNames } from '@/router/routes/auth'
import { ProfileRoute } from '@/router/routes/profile'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    DashboardRoute,
    SignInRoute,
    SignupRoute,
    ForgotPasswordRoute,
    ProfileRoute,
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
