import type { RouteRecordRaw } from 'vue-router'

import PageSignIn from '@/components/pages/SignIn.vue'
import PageSignup from '@/components/pages/Signup.vue'
import PageForgotPassword from '@/components/pages/ForgotPassword.vue'

export enum AuthRouteNames {
  SIGN_IN = 'SignIn',
  SIGNUP = 'Signup',
  FORGOT_PASSWORD = 'ForgotPassword',
}

export const SignInRoute: RouteRecordRaw = {
  name: AuthRouteNames.SIGN_IN,
  component: PageSignIn,
  path: '/signin',
}

export const SignupRoute: RouteRecordRaw = {
  name: AuthRouteNames.SIGNUP,
  component: PageSignup,
  path: '/signup',
}

export const ForgotPasswordRoute: RouteRecordRaw = {
  name: AuthRouteNames.FORGOT_PASSWORD,
  component: PageForgotPassword,
  path: '/forgot-password',
}
