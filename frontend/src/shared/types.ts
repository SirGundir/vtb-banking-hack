import { EBankName } from '@/shared/enums'

export type TBank = {
  id: string
  logo: string
  name: `${EBankName}`
  fullName: string
  ruName: string
  brandColor: string
  apiUrl: string
}

export type TBanks = TBank[]

export type TBankName = `${EBankName}`
