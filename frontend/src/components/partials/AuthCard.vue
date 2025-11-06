<template>
  <UiCard>
    <UiCardHeader>
      <UiCardTitle>
        {{ title }}
      </UiCardTitle>
      <UiCardDescription v-if="description">
        {{ description }}
      </UiCardDescription>
    </UiCardHeader>
    <UiCardContent>
      <slot name="content" />
    </UiCardContent>
    <UiCardFooter v-if="$slots.footer">
      <slot name="footer" />
    </UiCardFooter>
  </UiCard>
</template>

<script setup lang="ts">
import {
  Card as UiCard,
  CardHeader as UiCardHeader,
  CardTitle as UiCardTitle,
  CardDescription as UiCardDescription,
  CardContent as UiCardContent,
  CardFooter as UiCardFooter,
} from '@/components/ui/card'

defineOptions({
  name: 'PAuthCard',
})

defineProps<{
  title: string
  description?: string
}>()
</script>