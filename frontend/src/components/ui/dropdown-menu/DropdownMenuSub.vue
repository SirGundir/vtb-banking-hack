<script setup lang="ts">
import type { DropdownMenuSubEmits, DropdownMenuSubProps } from "reka-ui"
import {
  DropdownMenuSub,

  useForwardPropsEmits,
} from "reka-ui"

defineOptions({
  name: 'UiDropdownMenuSub',
})

const props = defineProps<DropdownMenuSubProps>()
const emits = defineEmits<DropdownMenuSubEmits>()

const forwarded = useForwardPropsEmits(props, emits)
</script>

<template>
  <DropdownMenuSub data-slot="dropdown-menu-sub" v-bind="forwarded">
    <slot />
  </DropdownMenuSub>
</template>
