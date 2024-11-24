<script setup lang="ts">
import { onMounted, ref, defineProps } from 'vue'

import * as d3 from 'd3'

import type { SummaryItem } from '@/types/Summary'
import useAnalyzeStore from '@/stores/AnalyzeStore'

const props = defineProps<{
  id_project: number | null
}>()

const store_analyze = useAnalyzeStore()

const is_enable_workload = ref(false)
const is_enable_item_workload = ref(false)
const is_enable_item_nunber = ref(false)

const value_workload = ref(0)
const value_item_workload = ref(0)
const value_item_number = ref(0)

enum SummaryType {
  NONE = 0,
  WORKLOAD,
  ITEM_WORKLOAD,
  ITEM_NUMBER
}

onMounted(async () => {
  await store_analyze.fetchSummaryProject(props.id_project)
  createChart()
})

function createChart() {
  const list_data = store_analyze.summaries_project
  if (!list_data || list_data.length === 0) {
    return
  }

  const max_value_workload = d3.max(list_data, (d: SummaryItem) =>
    Math.max(d.task_workload_total, d.bug_workload_total)
  ) as number
  const max_value_item_workload = d3.max(list_data, (d: SummaryItem) =>
    Math.max(d.task_count_total)
  ) as number
  const max_value_item_number = d3.max(list_data, (d: SummaryItem) =>
    Math.max(d.task_number_total)
  ) as number

  if (max_value_workload != 0) {
    is_enable_workload.value = true
  }
  if (max_value_item_workload != 0) {
    is_enable_item_workload.value = true
  }
  if (max_value_item_number != 0) {
    is_enable_item_nunber.value = true
  }

  d3.select(`#graph-workload`).selectAll('svg').remove()
  d3.select(`#graph-item-workload`).selectAll('svg').remove()
  d3.select(`#graph-item-number`).selectAll('svg').remove()

  const latest = list_data[list_data.length - 1]
  value_workload.value = latest.task_workload_total + latest.bug_workload_total
  value_item_workload.value = Math.floor(
    (latest.task_count_complete / latest.task_count_total) * 100
  )
  value_item_number.value = Math.floor(
    (latest.task_number_completed / latest.task_number_total) * 100
  )

  createChartDetail(SummaryType.WORKLOAD, list_data, max_value_workload, 3)
  createChartDetail(SummaryType.ITEM_WORKLOAD, list_data, max_value_item_workload, 0.3)
  createChartDetail(SummaryType.ITEM_NUMBER, list_data, max_value_item_number, 0.3)
}

function createChartDetail(
  type: SummaryType,
  data: SummaryItem[],
  max_value: number,
  margin: number
) {
  const date_end = d3.max(data, (d: any) => new Date(d.date_entry)) as Date
  const date_start = new Date(date_end)
  date_start.setDate(date_end.getDate() - 31)

  const width = 260
  const height = 80

  const x = d3.scaleTime().domain([date_start, date_end]).range([0, width])
  const y = d3
    .scaleLinear()
    .domain([0, max_value + margin])
    .nice()
    .range([height, 0])

  let svg: any
  let list_area: any[] = []

  switch (type) {
    case SummaryType.WORKLOAD:
      svg = d3.select(`#graph-workload`).append('svg')
      list_area = [
        {
          name: 'Total',
          value: (d: SummaryItem) => d.task_workload_total + d.bug_workload_total,
          color_line: 'rgba(180, 180, 180, 0.9)',
          color_area: 'rgba(180, 180, 180, 0.2)'
        }
      ]
      break

    case SummaryType.ITEM_WORKLOAD:
      svg = d3.select(`#graph-item-workload`).append('svg')
      list_area = [
        {
          name: 'Total',
          value: (d: SummaryItem) => d.task_count_total,
          color_line: 'rgba(116, 119, 176, 0.9)',
          color_area: 'rgba(116, 119, 176, 0.2)'
        },
        {
          name: 'Complete',
          value: (d: SummaryItem) => d.task_count_complete,
          color_line: 'rgba(90, 90, 90, 0.9)',
          color_area: 'rgba(90, 90, 90, 0.7)'
        }
      ]
      break

    case SummaryType.ITEM_NUMBER:
      svg = d3.select(`#graph-item-number`).append('svg')
      list_area = [
        {
          name: 'Total',
          value: (d: SummaryItem) => d.task_number_total,
          color_line: 'rgba(98, 163, 136, 0.9)',
          color_area: 'rgba(98, 163, 136, 0.2)'
        },
        {
          name: 'Complete',
          value: (d: SummaryItem) => d.task_number_completed,
          color_line: 'rgba(90, 90, 90, 0.9)',
          color_area: 'rgba(90, 90, 90, 0.7)'
        }
      ]
      break
  }

  svg.attr('width', width).attr('height', height).append('g')

  list_area.forEach((area) => {
    const areaPath = d3
      .area<SummaryItem>()
      .x((d: any) => x(new Date(d.date_entry)))
      .y0(y(0))
      .y1((d: any) => y(area.value(d)))
      .curve(d3.curveLinear)

    svg.append('path').datum(data).attr('fill', area.color_area).attr('d', areaPath)

    const linePath = d3
      .line<SummaryItem>()
      .x((d: any) => x(new Date(d.date_entry)))
      .y((d: any) => y(area.value(d)))
      .curve(d3.curveLinear)

    svg
      .append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', area.color_line)
      .attr('stroke-width', 1.2)
      .attr('d', linePath)
  })

  svg
    .append('g')
    .call(
      d3
        .axisBottom(x)
        .ticks(d3.timeDay.every(1))
        .tickFormat((domainValue: Date | d3.NumberValue) => {
          if (domainValue instanceof Date) {
            return d3.timeFormat('%m-%d')(domainValue)
          }
          return String(domainValue)
        })
        .tickSize(0)
    )
    .attr('transform', `translate(0,${height})`)
    .attr('color', '#393939')
    .attr('stroke-width', 2.5)
    .selectAll('text')
    .style('display', 'none')
}
</script>

<template>
  <v-container class="summary">
    <v-row>
      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">progress</div>
            <div class="title">
              <span>Workload</span>
              <span class="value" v-if="is_enable_workload">{{ value_workload }} pt</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" :id="`graph-workload`"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">completed rate</div>
            <div class="title">
              <span>Item : Workload</span>
              <span class="value" v-if="is_enable_item_workload">{{ value_item_workload }} %</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" :id="`graph-item-workload`"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">completed rate</div>
            <div class="title">
              <span>Item : Number</span>
              <span class="value" v-if="is_enable_item_nunber">{{ value_item_number }} %</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" :id="`graph-item-number`"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
@import '@/components/analyze/summary.css';
</style>
