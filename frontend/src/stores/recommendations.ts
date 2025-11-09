import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'

import { useApiConfig } from '@/composables/useApiConfig'
import { type JwtTokensDTO } from '@/api/models/JwtTokensDTO'
import { DefaultApi as RecomendationApi } from '@/api/apis/DefaultApi'
import { type ProductRecommendation } from '@/api/models/ProductRecommendation'


export const useRecommendationsStore = defineStore('recommendations', () => {
  const accessToken = useStorage<JwtTokensDTO['accessToken'] | null>('accessToken', null)
  const recommendations = ref<ProductRecommendation[]>([])
  const isGetRecommendationsLoading = ref(false)

  const getRecommendations = async () => {
    try {
      if (!accessToken.value) throw new Error('No access token')

      isGetRecommendationsLoading.value = true

      const config = useApiConfig()
      const recommendationsApi = new RecomendationApi(config)
      const response = await recommendationsApi
        .recommendStubApiV1RecommendClientIdPost({
          clientId: import.meta.env.VITE_CLIENT_ID,
          topN: 3,
          useMl: true,
        })

      recommendations.value = response

      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    } finally {
      isGetRecommendationsLoading.value = false
    }
  }

  return {
    recommendations,
    isGetRecommendationsLoading,
    getRecommendations,
  }
})
