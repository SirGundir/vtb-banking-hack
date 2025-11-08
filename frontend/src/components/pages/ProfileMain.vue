<template>
  <div class="flex flex-col gap-4">
    <div class="flex flex-col mb-4">
      <h1 class="text-lg font-medium mb-4">Основная информация</h1>
      <WUserInfo />
    </div>
    <div class="flex flex-col items-start gap-4">
      <h2 class="text-lg font-medium">Подключенные банки</h2>
      <WAvailableBanks />
    </div>
  </div>
</template>

<script setup lang="ts" name="PageProfileMain">
import WUserInfo from '@/components/widgets/UserInfo.vue'
import WAvailableBanks from '@/components/widgets/AvailableBanks.vue'

defineOptions({
  name: 'PageProfileMain',
})
</script>
