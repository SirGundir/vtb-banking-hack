import { computed } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

import { AuthApi } from '@/api/apis/AuthApi'
import { type LoginDTO } from '@/api/models/LoginDTO'
import { type JwtTokensDTO } from '@/api/models/JwtTokensDTO'

const api = new AuthApi()

export const useUserStore = defineStore('user', () => {
  const accessToken = useStorage<JwtTokensDTO['accessToken'] | null>('accessToken', null)
  const refreshToken = useStorage<JwtTokensDTO['refreshToken'] | null>('refreshToken', null)

  const isAuthenticated = computed(() => {
    return false
  })

  const signIn = async (credentials: LoginDTO) => {
    try {
      const response = await api.loginApiV1AuthLoginPost({ loginDTO: credentials })
      accessToken.value = response.accessToken
      refreshToken.value = response.refreshToken
      return Promise.resolve(response)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const signOut = async () => {
    try {
      if (!accessToken.value || !refreshToken.value) return

      await api.logoutApiV1AuthLogoutPost({ jwtTokensDTO: {
        accessToken: accessToken.value,
        refreshToken: refreshToken.value,
      } })
      accessToken.value = null
      refreshToken.value = null
      return Promise.resolve()
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  return {
    isAuthenticated,
    signIn,
    signOut,
  }
})
