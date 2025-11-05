import type { RouteRecordRaw } from 'vue-router'

import LayoutMe from '@/components/layouts/Me.vue'

import PageProfile from '@/components/pages/Profile.vue'
import PageDashboard from '@/components/pages/Dashboard.vue'
import PageDeposit from '@/components/pages/Deposit.vue'
import PageAccount from '@/components/pages/Account.vue'
import PageCard from '@/components/pages/Card.vue'
import PageLoan from '@/components/pages/Loan.vue'

export enum MeRouteNames {
  ME = 'Me',
  DASHBOARD = 'Dashboard',
  PROFILE = 'Profile',
  DEPOSIT = 'Deposit',
  ACCOUNT = 'Account',
  CARD = 'Card',
  LOAN = 'Loan',
}

export const MeProfileRoute: RouteRecordRaw = {
  name: MeRouteNames.PROFILE,
  component: PageProfile,
  path: 'profile',
  meta: {
    auth: true,
  },
}

export const MeDashboardRoute: RouteRecordRaw = {
  name: MeRouteNames.DASHBOARD,
  component: PageDashboard,
  path: 'dashboard',
  meta: {
    auth: true,
  },
}

export const MeDepositRoute: RouteRecordRaw = {
  name: MeRouteNames.DEPOSIT,
  component: PageDeposit,
  path: 'deposit',
  meta: {
    auth: true,
  },
}

export const MeAccountRoute: RouteRecordRaw = {
  name: MeRouteNames.ACCOUNT,
  component: PageAccount,
  path: 'account',
  meta: {
    auth: true,
  },
}

export const MeCardRoute: RouteRecordRaw = {
  name: MeRouteNames.CARD,
  component: PageCard,
  path: 'card',
  meta: {
    auth: true,
  },
}

export const MeLoanRoute: RouteRecordRaw = {
  name: MeRouteNames.LOAN,
  component: PageLoan,
  path: 'loan',
  meta: {
    auth: true,
  },
}

export const MeRoute: RouteRecordRaw = {
  name: MeRouteNames.ME,
  path: '/me',
  redirect: { name: MeRouteNames.DASHBOARD },
  component: LayoutMe,
  children: [
    MeProfileRoute,
    MeDashboardRoute,
    MeDepositRoute,
    MeAccountRoute,
    MeCardRoute,
    MeLoanRoute,
  ],
}
