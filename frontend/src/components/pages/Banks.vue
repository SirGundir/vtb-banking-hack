<template>
  <div class="flex flex-col items-start gap-4">
    <div class="flex flex-col mb-4">
      <h1 class="text-xl font-medium mb-2">Доступные банки</h1>
      <p class="text-sm text-muted-foreground">Выберите банки, которые вы хотите подключить к своему аккаунту</p>
    </div>
    <WAvailableBanks />
  </div>
</template>

<script setup lang="ts">
import WAvailableBanks from '@/components/widgets/AvailableBanks.vue'

defineOptions({
  name: 'PageBanks',
})
</script>
