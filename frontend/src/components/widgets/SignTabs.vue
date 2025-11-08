<template>
  <div class="items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground grid w-full grid-cols-2">
    <template v-for="link in links" :key="link.label">
      <component :is="link.as" :to="link.to" :class="link.buttonProps.class">
        <UiButton :variant="link.buttonProps.variant" :class="link.buttonProps.class">
          {{ link.label }}
        </UiButton>
      </component>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, type HTMLAttributes } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import { Button as UiButton, type ButtonVariants } from '@/components/ui/button'
import { AuthRouteNames } from '@/router/routes/auth'

defineOptions({
  name: 'WSignTabs',
})

type ButtonProps = ButtonVariants & {
  class?: HTMLAttributes['class']
}

const route = useRoute()

const getButtonProps = (isActive: boolean): ButtonProps => {
  return {
    variant: isActive ? 'default' : 'ghost',
    class: 'w-full',
  }
}

const links = computed(() => {
  const isSignIn = route.name === AuthRouteNames.SIGN_IN
  const isSignup = route.name === AuthRouteNames.SIGNUP

  return [
    {
      label: 'Вход',
      to: { name: AuthRouteNames.SIGN_IN },
      as: isSignIn ? 'span' : RouterLink,
      isActive: isSignIn,
      buttonProps: getButtonProps(isSignIn),
    },
    {
      label: 'Регистрация',
      to: { name: AuthRouteNames.SIGNUP },
      as: isSignup ? 'span' : RouterLink,
      isActive: isSignup,
      buttonProps: getButtonProps(isSignup),
    },
  ]
})
</script>