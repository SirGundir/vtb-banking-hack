<template>
  <div class="__app">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { provide } from 'vue'

import { useResize } from '@/composables/useResize'

const { vh } = useResize()

provide('vh', vh)
</script>

<style lang="postcss">
.__app {
  @apply flex min-h-screen;

  min-height: calc(var(--vh, 1vh) * 100);

  & > * {
    @apply flex w-full flex-col;
  }
}
</style>