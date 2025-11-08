import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

import { AuthApi } from '@/api/apis/AuthApi'
import { UsersApi } from '@/api/apis/UsersApi'
import { type UserSchema } from '@/api/models/UserSchema'
import { type LoginDTO } from '@/api/models/LoginDTO'
import { type JwtTokensDTO } from '@/api/models/JwtTokensDTO'
import { type CreateUserDTO } from '@/api/models/CreateUserDTO'
import { useApiConfig } from '@/composables/useApiConfig'

const authApi = new AuthApi()

export const useUserStore = defineStore('user', () => {
  const user = ref<UserSchema | null>(null)
  const isGetMeLoading = ref(false)

  const accessToken = useStorage<JwtTokensDTO['accessToken'] | null>('accessToken', null)
  const refreshToken = useStorage<JwtTokensDTO['refreshToken'] | null>('refreshToken', null)

  const isAuthenticated = computed(() => {
    return !!accessToken.value && !!refreshToken.value && user.value !== null
  })

  const hasConnectedBanks = computed(() => {
    return (user.value?.connectedBanks.length ?? 0) > 0
  })

  const connectedBanks = computed(() => {
    return user.value?.connectedBanks ?? []
  })

  /**
   * Вход в систему
   * @param credentials - Логин и пароль
   * @returns Токены доступа и обновления
   */
  const signIn = async (credentials: LoginDTO) => {
    try {
      const response = await authApi.loginApiV1AuthLoginPost({ loginDTO: credentials })
      accessToken.value = response.accessToken
      refreshToken.value = response.refreshToken
      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    }
  }

  /**
   * Регистрация
   * @param userData - Данные пользователя
   * @returns Токены доступа и обновления
   */
  const signUp = async (userData: CreateUserDTO) => {
    try {
      const response = await authApi.signupApiV1AuthSignupPost({ createUserDTO: userData })
      accessToken.value = response.accessToken
      refreshToken.value = response.refreshToken
      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    }
  }

  /**
   * Выход из системы
   */
  const signOut = async () => {
    try {
      if (!accessToken.value || !refreshToken.value) return

      await authApi.logoutApiV1AuthLogoutPost({ jwtTokensDTO: {
        accessToken: accessToken.value,
        refreshToken: refreshToken.value,
      } })

      return Promise.resolve()
    } catch (error) {
      console.error(error)
    } finally {
      accessToken.value = null
      refreshToken.value = null
      user.value = null
    }
  }

  /**
   * Обновление токена доступа
   */
  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) throw new Error('No refresh token')

      const response = await authApi.refreshApiV1AuthRefreshPost({
        refreshTokenDTO: {
          refreshToken: refreshToken.value,
        },
      })

      accessToken.value = response.accessToken
      refreshToken.value = response.refreshToken

      return Promise.resolve(response)
    } catch (error: unknown) {
      return Promise.reject(error)
    }
  }

  /**
   * Получение информации о пользователе
   * @returns Информация о пользователе
   */
  const getMe = async (): Promise<UserSchema> => {
    try {
      if (!accessToken.value) throw new Error('No access token')
        
      isGetMeLoading.value = true
      const config = useApiConfig()
      const usersApi = new UsersApi(config)
      const response = await usersApi.getMeApiV1UsersMeGet()
  
      user.value = response
  
      return response
    } catch (error) {
      return Promise.reject(error)
    } finally {
      isGetMeLoading.value = false
    }
  }

  /**
   * Сброс email
   * @param email - Email
   * @returns Токены доступа и обновления
   */
  const resetEmail = async (email: string) => {
    try {
      const response = await authApi.startResetPasswordApiV1AuthResetStartPost({
        resetPasswordDTO: {
          email,
        },
      })
      return Promise.resolve(response)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  return {
    user,
    isGetMeLoading,
    accessToken,
    refreshToken,
    isAuthenticated,
    hasConnectedBanks,
    connectedBanks,
    signIn,
    signUp,
    signOut,
    getMe,
    refreshAccessToken,
    resetEmail,
  }
})
