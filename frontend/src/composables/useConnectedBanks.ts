import { computed } from 'vue'
import { storeToRefs } from 'pinia'

import { AVAILABLE_BANKS } from '@/shared/constants'
import { useUserStore } from '@/stores/user'
import { useBanksStore } from '@/stores/banks'

export const useConnectedBanks = () => {
  const userStore = useUserStore()
  const { user } = storeToRefs(userStore)
  const banksStore = useBanksStore()
  const { banks } = storeToRefs(banksStore)

  const connectedBanks = computed(() => {
    return AVAILABLE_BANKS.filter(availableBank => {
      return (banks.value ?? [])
        .filter(bank => user.value?.connectedBanks.includes(bank.id))
        .some(bank => bank.name === availableBank.name)
    })
  })

  return {
    connectedBanks,
  }
}
