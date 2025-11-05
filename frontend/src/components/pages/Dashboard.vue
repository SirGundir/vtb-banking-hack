<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <WidgetInOut />
  </div>
</template>

<script setup lang="ts">
import WidgetInOut from '@/components/widgets/InOut.vue'

defineOptions({
  name: 'PageDashboard',
})
</script>
