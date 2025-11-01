import { useRouter } from 'vue-router'

import { AuthRouteNames } from '@/router/routes/auth'
import { Configuration, type Middleware, type ErrorContext } from '@/api/runtime'
import { useUserStore } from '@/stores/user'

let refreshPromise: Promise<void> | null = null

/**
 * Создает middleware для автоматической обработки протухания токена
 */
function createAuthMiddleware(): Middleware {
  return {
    async onError(context: ErrorContext) {
      const { response, url, init } = context
      
      // Пропускаем обработку для эндпоинтов авторизации и рефреша
      if (
        url.includes('/auth/login') ||
        url.includes('/auth/signup') ||
        url.includes('/auth/refresh') ||
        url.includes('/auth/reset')
      ) {
        return response
      }

      // Обрабатываем только 401 ошибки
      if (response?.status === 401) {
        const userStore = useUserStore()

        // Предотвращаем множественные одновременные попытки обновления токена
        if (!refreshPromise) {
          refreshPromise = (async () => {
            try {
              await userStore.refreshAccessToken()
            } catch (error: unknown) {
              console.error(error)

              // Пытаемся выйти из аккаунта
              try {
                await userStore.signOut()
                useRouter().push({ name: AuthRouteNames.SIGN_IN })
              } catch (error: unknown) {
                throw error
              }
            } finally {
              refreshPromise = null
            }
          })()
        }

        try {
          // Ждем обновления токена
          await refreshPromise

          // Повторяем оригинальный запрос с новым токеном
          const newToken = userStore.accessToken
          if (!newToken) {
            throw new Error('Failed to refresh token')
          }

          // Обновляем заголовок Authorization в запросе
          const newInit = { ...init }
          const headers = new Headers(newInit.headers)
          headers.set('Authorization', `Bearer ${newToken}`)
          newInit.headers = headers

          // Повторяем запрос
          return await fetch(url, newInit)
        } catch (error: unknown) {
          console.error(error)
          // Если обновление не удалось, возвращаем оригинальный response
          return response
        }
      }

      return response
    },
  }
}

/**
 * Создает конфигурацию API с автоматической обработкой токена
 */
export function useApiConfig(): Configuration {
  const userStore = useUserStore()

  return new Configuration({
    // accessToken как функция, чтобы всегда получать актуальный токен
    accessToken: () => userStore.accessToken || '',
    middleware: [createAuthMiddleware()],
  })
}
