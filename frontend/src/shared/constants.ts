import { CalendarDate } from '@internationalized/date'

import { type TBanks } from '@/shared/types'
import { EBankName } from '@/shared/enums'

export const AVAILABLE_BANKS: TBanks = [
  {
    id: 'VB',
    logo: '🏦',
    name: EBankName.VIRTUAL_BANK,
    fullName: 'Virtual Bank',
    ruName: 'Виртуальный Банк',
    brandColor: '#5e8aff',
    apiUrl: 'https://vbank.open.bankingapi.ru',
  },
  {
    id: 'AB',
    logo: '🏦',
    name: EBankName.AWESOME_BANK,
    fullName: 'Awesome Bank',
    ruName: 'Потрясающий банк',
    brandColor: '#ff4088',
    apiUrl: 'https://abank.open.bankingapi.ru',
  },
  {
    id: 'SB',
    logo: '🏦',
    name: EBankName.SMART_BANK,
    fullName: 'Smart Bank',
    ruName: 'Умный банк',
    brandColor: '#1ec99b',
    apiUrl: 'https://sbank.open.bankingapi.ru',
  },
]

export const CLIENT_ID = 'team221'
export const CLIENT_SECRET = 'uLICRPukXIX7EvwS49xgEuDEByZXfMVw'

export const CURRENT_CALENDAR_DATE = new CalendarDate(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())

export const DEFAULT_START_DATE = CURRENT_CALENDAR_DATE.subtract({ days: 20 }).toDate('UTC')
export const DEFAULT_END_DATE = CURRENT_CALENDAR_DATE.toDate('UTC')
