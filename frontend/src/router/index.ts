import { createRouter, createWebHistory } from 'vue-router'

import { HomeRoute } from '@/router/routes/home'
import { SignInRoute, SignupRoute, ForgotPasswordRoute } from '@/router/routes/auth'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    HomeRoute,
    SignInRoute,
    SignupRoute,
    ForgotPasswordRoute,
  ],
})

router.beforeEach((to, from, next) => {
  if (!to.meta.auth) return next()

  const { isAuthenticated } = useUserStore()

  if (!isAuthenticated) {
    next({ path: '/signin' })
  }

  next()
})

export default router
