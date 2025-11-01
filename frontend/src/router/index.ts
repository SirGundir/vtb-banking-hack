import { createRouter, createWebHashHistory } from 'vue-router'

import { HomeRoute, HomeRouteNames } from '@/router/routes/home'
import { SignInRoute, SignupRoute, ForgotPasswordRoute, AuthRouteNames } from '@/router/routes/auth'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    HomeRoute,
    SignInRoute,
    SignupRoute,
    ForgotPasswordRoute,
  ],
})

const redirectedToHomeRoutes = [
  AuthRouteNames.SIGN_IN,
  AuthRouteNames.SIGNUP,
  AuthRouteNames.FORGOT_PASSWORD,
]

router.beforeEach(async (to, from, next) => {
  if (!to.meta.auth) return next()

  const userStore = useUserStore()

  if (!userStore.user) {
    try {
      await userStore.getMe()
      if (redirectedToHomeRoutes.includes(to.name as AuthRouteNames)) {
        return next({ name: HomeRouteNames.HOME })
      }
    } catch (error: unknown) {
      console.error(error)
      return next({ name: AuthRouteNames.SIGN_IN })
    }
  }

  return next()
})

export default router
