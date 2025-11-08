import type { RouteRecordRaw } from 'vue-router'

import LayoutOnboarding from '@/components/layouts/Onboarding.vue'

import PageBanks from '@/components/pages/Banks.vue'
import PageSurvey from '@/components/pages/Survey.vue'

export enum OnboardingRouteNames {
  ONBOARDING = 'Onboarding',
  BANKS = 'Banks',
  SURVEY = 'Survey',
}

export const OnboardingBanksRoute: RouteRecordRaw = {
  name: OnboardingRouteNames.BANKS,
  component: PageBanks,
  path: 'banks',
  meta: {
    auth: true,
  },
}

export const OnboardingSurveyRoute: RouteRecordRaw = {
  name: OnboardingRouteNames.SURVEY,
  component: PageSurvey,
  path: 'survey',
  meta: {
    auth: true,
  },
}

export const OnboardingRoute: RouteRecordRaw = {
  name: OnboardingRouteNames.ONBOARDING,
  path: '/onboarding',
  redirect: { name: OnboardingRouteNames.BANKS },
  component: LayoutOnboarding,
  children: [
    OnboardingBanksRoute,
    OnboardingSurveyRoute,
  ],
}
