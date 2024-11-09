<script setup lang="ts">
import { onMounted, ref, defineProps } from 'vue'

import * as d3 from 'd3'

import type { SummaryItem } from '@/types/Summary'
import useProgressStore from '@/stores/ProgressStore'

const props = defineProps<{
  id_project: number | null
  rid_users: number
}>()

const store_progress = useProgressStore()

const is_enable_workload = ref(false)
const is_enable_bug = ref(false)
const is_enable_alert = ref(false)

const value_workload = ref(0)
const value_bug = ref(0)
const value_alert = ref(0)

enum SummaryType {
  NONE = 0,
  WORKLOAD,
  BUG,
  RISK
}

onMounted(async () => {
  await store_progress.fetchSummariesUser(props.id_project, props.rid_users)
  createChart()
})

function createChart() {
  const list_data = store_progress.summaries_user.get(props.rid_users)
  if (!list_data || list_data.length === 0) {
    return
  }

  const max_value_workload = d3.max(list_data, (d: SummaryItem) =>
    Math.max(d.task_workload_total, d.bug_workload_total)
  ) as number
  const max_value_bug = d3.max(list_data, (d: SummaryItem) => Math.max(d.bug_count_total)) as number
  const max_value_alert = d3.max(
    list_data,
    (d: SummaryItem) => Math.max(d.task_count_alert) + Math.max(d.bug_count_alert)
  ) as number

  if (max_value_workload != 0) {
    is_enable_workload.value = true
  }
  if (max_value_bug != 0) {
    is_enable_bug.value = true
  }
  if (max_value_alert != 0) {
    is_enable_alert.value = true
  }

  d3.select(`#graph-bug-workload`).selectAll('svg').remove()
  d3.select(`#graph-bug`).selectAll('svg').remove()
  d3.select(`#graph-alert`).selectAll('svg').remove()

  const latest = list_data[list_data.length - 1]
  value_workload.value = latest.bug_workload_total
  value_bug.value = Math.floor((latest.bug_count_complete / latest.bug_count_total) * 100)
  value_alert.value = latest.task_count_alert + latest.bug_count_alert

  createChartDetail(SummaryType.WORKLOAD, list_data, max_value_workload)
  createChartDetail(SummaryType.BUG, list_data, max_value_bug)
  createChartDetail(SummaryType.RISK, list_data, max_value_alert)
}

function createChartDetail(type: SummaryType, data: SummaryItem[], max_value: number) {
  const date_end = d3.max(data, (d: any) => new Date(d.date_entry)) as Date
  const date_start = new Date(date_end)
  date_start.setDate(date_end.getDate() - 21)

  const width = 260
  const height = 80

  const x = d3.scaleTime().domain([date_start, date_end]).range([0, width])

  let svg: any
  let list_area: any[] = []
  let yScales: any[] = []

  switch (type) {
    case SummaryType.WORKLOAD: {
      svg = d3.select(`#graph-bug-workload`).append('svg')
      const y_workload = d3
        .scaleLinear()
        .domain([0, (max_value as number) + 2])
        .nice()
        .range([height, 0])
      yScales = [y_workload, y_workload]
      list_area = [
        {
          name: 'Total',
          value: (d: SummaryItem) => d.bug_workload_total,
          color_line: 'rgba(180, 180, 180, 0.9)',
          color_area: 'rgba(180, 180, 180, 0.2)'
        }
      ]
      break
    }

    case SummaryType.BUG: {
      svg = d3.select(`#graph-bug`).append('svg')
      const y_bug = d3
        .scaleLinear()
        .domain([0, (max_value as number) + 2])
        .nice()
        .range([height, 0])
      yScales = [y_bug, y_bug]
      list_area = [
        {
          name: 'Total',
          value: (d: SummaryItem) => d.bug_count_total,
          color_line: 'rgba(120, 92, 10, 0.9)',
          color_area: 'rgba(120, 92, 10, 0.2)'
        },
        {
          name: 'Complete',
          value: (d: SummaryItem) => d.bug_count_complete,
          color_line: 'rgba(90, 90, 90, 0.9)',
          color_area: 'rgba(90, 90, 90, 0.7)'
        }
      ]
      break
    }

    case SummaryType.RISK: {
      svg = d3.select(`#graph-alert`).append('svg')
      const y_risk = d3
        .scaleLinear()
        .domain([0, (max_value as number) + 2])
        .nice()
        .range([height, 0])
      const y_alert = d3
        .scaleLinear()
        .domain([0, (max_value as number) + 2])
        .nice()
        .range([height, 0])
      yScales = [y_risk, y_alert]
      list_area = [
        {
          name: 'Risk',
          value: (d: SummaryItem) => d.risk,
          color_line: 'rgba(156, 145, 81, 0.9)',
          color_area: 'rgba(156, 145, 81, 0.2)'
        },
        {
          name: 'Alert',
          value: (d: SummaryItem) => d.task_count_alert + d.bug_count_alert,
          color_line: 'rgba(181, 48, 69, 0.9)',
          color_area: 'rgba(181, 48, 69, 0.2)'
        }
      ]
      break
    }
  }

  svg.attr('width', width).attr('height', height).append('g')

  list_area.forEach((area, index) => {
    const yScale = yScales[index]

    const areaPath = d3
      .area<SummaryItem>()
      .x((d: any) => x(new Date(d.date_entry)))
      .y0(yScale(0))
      .y1((d: any) => yScale(area.value(d)))
      .curve(d3.curveLinear)

    svg.append('path').datum(data).attr('fill', area.color_area).attr('d', areaPath)

    const linePath = d3
      .line<SummaryItem>()
      .x((d: any) => x(new Date(d.date_entry)))
      .y((d: any) => yScale(area.value(d)))
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
            <div class="graph" :id="`graph-bug-workload`"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">completed rate</div>
            <div class="title">
              <span>Bug</span>
              <span class="value" v-if="is_enable_bug">{{ value_bug }} %</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" :id="`graph-bug`"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">caution</div>
            <div class="title">
              <span>Risk & Alert</span>
              <span class="value" v-if="is_enable_alert">{{ value_alert }} alert</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" :id="`graph-alert`"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
@import '@/components/analyze/summary.css';
</style>
