<template>
  <div class="relative">
    <ChartPie
      :data="data"
      :options="options"
    />
  </div>
</template>

<script setup lang="ts">
import { Chart as ChartJS, ArcElement, Tooltip, Legend, } from 'chart.js'
import { Pie as ChartPie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

defineOptions({
  name: 'PPieChart',
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
}

enum EBanks {
  VTB = 'vtb',
  ALFA = 'alfa',
  SBER = 'sber',
  TBANK = 'tbank',
}

const mapBankToLabel: Record<EBanks, string> = {
  [EBanks.VTB]: 'ВТБ',
  [EBanks.ALFA]: 'Альфа-Банк',
  [EBanks.SBER]: 'Сбербанк',
  [EBanks.TBANK]: 'ТБанк',
}

const mapBankToColor: Record<EBanks, string> = {
  [EBanks.VTB]: '#0A2896',
  [EBanks.ALFA]: '#ef3124',
  [EBanks.SBER]: '#21A038',
  [EBanks.TBANK]: '#FFDD2D',
}

const data = {
  labels: [
    mapBankToLabel[EBanks.VTB],
    mapBankToLabel[EBanks.ALFA],
    mapBankToLabel[EBanks.SBER],
    mapBankToLabel[EBanks.TBANK],
  ],
  datasets: [
    {
      backgroundColor: [
        mapBankToColor[EBanks.VTB],
        mapBankToColor[EBanks.ALFA],
        mapBankToColor[EBanks.SBER],
        mapBankToColor[EBanks.TBANK],
      ],
      data: [
        40,
        20,
        80,
        60,
      ],
    }
  ],
}
</script>