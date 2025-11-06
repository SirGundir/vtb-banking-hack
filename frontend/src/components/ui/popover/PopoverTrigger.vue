<script setup lang="ts">
import type { PopoverTriggerProps } from "reka-ui"
import { PopoverTrigger } from "reka-ui"

defineOptions({
  name: 'UiPopoverTrigger',
})

const props = defineProps<PopoverTriggerProps>()
</script>

<template>
  <PopoverTrigger
    data-slot="popover-trigger"
    v-bind="props"
  >
    <slot />
  </PopoverTrigger>
</template>
