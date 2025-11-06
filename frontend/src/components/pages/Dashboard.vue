<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <WDebitsAndReceipts />
    <WDebitsCategories />
  </div>
</template>

<script setup lang="ts">
import WDebitsAndReceipts from '@/components/widgets/DebitsAndReceipts.vue'
import WDebitsCategories from '@/components/widgets/DebitsCategories.vue'

defineOptions({
  name: 'PageDashboard',
})
</script>
