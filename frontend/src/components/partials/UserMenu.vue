<template>
  <UiDropdownMenu>
    <UiDropdownMenuTrigger as-child>
      <UiAvatar class="cursor-pointer">
        <UiAvatarFallback>{{ initials }}</UiAvatarFallback>
      </UiAvatar>
    </UiDropdownMenuTrigger>
    <UiDropdownMenuContent>
      <UiDropdownMenuItem as-child>
        <RouterLink to="/profile" class="cursor-pointer w-full">
          Настройки профиля
        </RouterLink>
      </UiDropdownMenuItem>
      <UiDropdownMenuSeparator />
      <UiDropdownMenuItem as-child>
        <button @click="logout" class="cursor-pointer w-full">
          Выйти
        </button>
      </UiDropdownMenuItem>
    </UiDropdownMenuContent>
  </UiDropdownMenu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import {
  DropdownMenu as UiDropdownMenu,
  DropdownMenuTrigger as UiDropdownMenuTrigger,
  DropdownMenuContent as UiDropdownMenuContent,
  DropdownMenuSeparator as UiDropdownMenuSeparator,
  DropdownMenuItem as UiDropdownMenuItem,
} from '@/components/ui/dropdown-menu'
import {
  Avatar as UiAvatar,
  AvatarFallback as UiAvatarFallback,
} from '@/components/ui/avatar'

import { useUserStore } from '@/stores/user'
import { AuthRouteNames } from '@/router/routes/auth'

defineOptions({
  name: 'PartialUserMenu',
})

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const router = useRouter()

const initials = computed(() => {
  return (user.value?.firstName?.charAt(0) || '') + (user.value?.lastName?.charAt(0) || '') || 'FL'
})

const logout = async () => {
  await userStore.signOut()
  router.push({ name: AuthRouteNames.SIGN_IN })
}
</script>