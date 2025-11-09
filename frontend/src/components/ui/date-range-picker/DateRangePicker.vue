<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        :class="cn(
          'w-[280px] justify-start text-left font-normal',
          !value && 'text-muted-foreground',
        )"
      >
        <CalendarIcon class="mr-2 size-4" />
        <template v-if="value?.start">
          <template v-if="value?.end">
            {{ df.format(value.start.toDate(getLocalTimeZone())) }} - {{ df.format(value.end.toDate(getLocalTimeZone())) }}
          </template>

          <template v-else>
            {{ df.format(value.start.toDate(getLocalTimeZone())) }}
          </template>
        </template>
        <template v-else>
          Выберите дату
        </template>
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-auto p-0">
      <RangeCalendar
        v-model="value"
        initial-focus
        locale="ru-RU"
        :number-of-months="2"
        weekday-format="short"
        @update:start-value="(startDate) => value.start = startDate"
      />
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import { computed } from "vue"
import type { DateRange } from "reka-ui"

import {
  CalendarDate,
  DateFormatter,
  getLocalTimeZone,
} from "@internationalized/date"
import { CalendarIcon } from "lucide-vue-next"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { RangeCalendar } from "@/components/ui/range-calendar"

const df = new DateFormatter('ru-RU', {
  dateStyle: 'medium',
})

const {
  start,
  end,
} = defineProps<{
  start?: Date
  end?: Date
}>()

const emits = defineEmits<{
  (event: 'update:start', value?: Date): void
  (event: 'update:end', value?: Date): void
}>()

const value = computed<DateRange>({
  get() {
    const dStart = start ? new Date(start) : undefined
    const dEnd = end ? new Date(end) : undefined

    return {
      start: dStart ? new CalendarDate(dStart.getFullYear(), dStart.getMonth(), dStart.getDate()) : undefined,
      end: dEnd ? new CalendarDate(dEnd.getFullYear(), dEnd.getMonth(), dEnd.getDate()) : undefined,
    }
  },
  set(value: DateRange) {
    emits('update:start', value.start?.toDate('UTC'))
    emits('update:end', value.end?.toDate('UTC'))
  },
})
</script>
