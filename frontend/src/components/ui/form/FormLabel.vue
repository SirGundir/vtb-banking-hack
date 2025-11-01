<script lang="ts" setup>
import type { LabelProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { Label } from '@/components/ui/label'
import { useFormField } from "./useFormField"

defineOptions({
  name: 'UiFormLabel',
})

const props = defineProps<LabelProps & { class?: HTMLAttributes["class"], required?: boolean }>()

const { error, formItemId } = useFormField()
</script>

<template>
  <Label
    data-slot="form-label"
    :data-error="!!error"
    :class="cn(
      'data-[error=true]:text-destructive',
      props.class,
    )"
    :for="formItemId"
  >
    <slot />

    <sup v-if="required" class="text-destructive font-bold">*</sup>
  </Label>
</template>
