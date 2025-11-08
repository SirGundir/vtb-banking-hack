<template>
  <div class="flex flex-col gap-2">
    <div class="flex flex-col gap-1">
      <span class="text-sm text-muted-foreground">Имя</span>
      <span class="font-medium">{{ user?.firstName }}</span>
    </div>
    <div class="flex flex-col gap-1">
      <span class="text-sm text-muted-foreground">Фамилия</span>
      <span class="font-medium">{{ user?.lastName }}</span>
    </div>
    <div class="flex flex-col gap-1">
      <span class="text-sm text-muted-foreground">Email</span>
      <div class="flex items-center gap-2 h-8">
        <span class="font-medium">{{ user?.email }}</span>
        <UiSeparator orientation="vertical" />
        <div v-if="user?.emailVerified" class="flex items-center gap-2">
          <CheckCircle class="size-4 text-green-500" />
          <span class="text-sm text-muted-foreground">Email подтвержден</span>
        </div>
        <UiButton v-else variant="outline" size="sm" class="w-fit">
          <MailIcon class="size-4" />
          Подтвердить email
        </UiButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MailIcon, CheckCircle } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/stores/user'

import { Button as UiButton } from '@/components/ui/button'
import { Separator as UiSeparator } from '@/components/ui/separator'

defineOptions({
  name: 'WUserInfo',
})

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
</script>
