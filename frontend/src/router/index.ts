import { createRouter, createWebHashHistory } from 'vue-router'
import { toast } from 'vue-sonner'

import { MeRoute } from '@/router/routes/me'
import {
  OnboardingRoute,
} from '@/router/routes/onboarding'
import { AuthRoute } from '@/router/routes/auth'
import { MeRouteNames, AuthRouteNames } from '@/shared/enums'
import {
  ProfileRoute,
} from '@/router/routes/profile'
import { useUserStore } from '@/stores/user'
import { ResponseError } from '@/api/runtime'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: { name: MeRouteNames.ME },
    },
    MeRoute,
    AuthRoute,
    OnboardingRoute,
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
      if (error instanceof ResponseError) {
        const errorData = await (error as ResponseError).response.json()

        toast.error(errorData.detail)
      } else {
        toast.error('Неизвестная ошибка')
      }

      return next({ name: AuthRouteNames.SIGN_IN })
    }
  }

  return next()
})

export default router
