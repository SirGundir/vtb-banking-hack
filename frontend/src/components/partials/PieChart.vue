<template>
  <div class="relative">
    <ChartPie
      :data="data"
      :options="options"
    />
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  type ChartData,
} from 'chart.js'
import { Pie as ChartPie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

defineOptions({
  name: 'PPieChart',
})

const {
  data = {
    labels: [],
    datasets: [],
  },
} = defineProps<{
  data?: ChartData<'pie'>
}>()

const options = {
  responsive: true,
  maintainAspectRatio: false,
}
</script>