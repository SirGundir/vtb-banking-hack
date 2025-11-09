<template>
  <div class="relative">
    <ChartBar
      :data="data"
      :options="options"
    />
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  type ChartData,
} from 'chart.js'
import { Bar as ChartBar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

defineOptions({
  name: 'PStackedBarChart',
})

const {
  data = {
    labels: [],
    datasets: [],
  },
} = defineProps<{
  data?: ChartData<'bar'>
}>()

const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true
    },
  },
}

// enum EBanks {
//   VTB = 'vtb',
//   ALFA = 'alfa',
//   SBER = 'sber',
//   TBANK = 'tbank',
// }

// enum ECategories {
//   FOOD = 'food',
//   TRANSPORT = 'transport',
//   HOUSING = 'housing',
//   UTILITIES = 'utilities',
//   OTHER = 'other',
// }

// const mapCategoryToLabel: Record<ECategories, string> = {
//   [ECategories.FOOD]: 'Еда',
//   [ECategories.TRANSPORT]: 'Транспорт',
//   [ECategories.HOUSING]: 'Жилье',
//   [ECategories.UTILITIES]: 'Коммунальные услуги',
//   [ECategories.OTHER]: 'Другое',
// }

// const mapBankToLabel: Record<EBanks, string> = {
//   [EBanks.VTB]: 'ВТБ',
//   [EBanks.ALFA]: 'Альфа-Банк',
//   [EBanks.SBER]: 'Сбербанк',
//   [EBanks.TBANK]: 'ТБанк',
// }

// const mapBankToColor: Record<EBanks, string> = {
//   [EBanks.VTB]: '#0A2896',
//   [EBanks.ALFA]: '#ef3124',
//   [EBanks.SBER]: '#21A038',
//   [EBanks.TBANK]: '#FFDD2D',
// }

// const data = {
//   labels: [
//     mapCategoryToLabel[ECategories.FOOD],
//     mapCategoryToLabel[ECategories.TRANSPORT],
//     mapCategoryToLabel[ECategories.HOUSING],
//     mapCategoryToLabel[ECategories.UTILITIES],
//     mapCategoryToLabel[ECategories.OTHER],
//   ],
//   datasets: [
//     {
//       label: mapBankToLabel[EBanks.VTB],
//       data: [
//         40,
//         20,
//         80,
//         60,
//         10,
//       ],
//       backgroundColor: mapBankToColor[EBanks.VTB],
//     },
//     {
//       label: mapBankToLabel[EBanks.ALFA],
//       data: [
//         20,
//         40,
//         60,
//         80,
//         30,
//       ],
//       backgroundColor: mapBankToColor[EBanks.ALFA],
//     },
//     {
//       label: mapBankToLabel[EBanks.SBER],
//       data: [
//         80,
//         60,
//         40,
//         20,
//         25,
//       ],
//       backgroundColor: mapBankToColor[EBanks.SBER],
//     },
//     {
//       label: mapBankToLabel[EBanks.TBANK],
//       data: [
//         60,
//         80,
//         20,
//         40,
//         50,
//       ],
//       backgroundColor: mapBankToColor[EBanks.TBANK],
//     },
//   ],
// }
</script>