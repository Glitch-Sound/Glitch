<script setup lang="ts">
import { defineProps } from 'vue'

import * as d3 from 'd3'

import type { SummaryItem } from '@/types/Summary'
import { useSummaryChart, SummaryType } from '@/components/analyze/SummaryChart'

const props = defineProps<{
  id_project: number | null
  rid_users: number
}>()

const chartConfigs = [
  {
    type: SummaryType.WORKLOAD,
    selector: '#graph-item-workload',
    isEnableKey: 'workload',
    valueKey: 'workload',
    maxValueFunc: (data: SummaryItem[]) =>
      d3.max(data, (d: SummaryItem) => Math.max(d.task_workload_total, d.bug_workload_total)) || 0,
    valueFunc: (latest: SummaryItem) => latest.task_workload_total,
    list_area: [
      {
        name: 'Total',
        value: (d: SummaryItem) => d.task_workload_total,
        color_line: 'rgba(180, 180, 180, 0.9)',
        color_area: 'rgba(180, 180, 180, 0.2)'
      }
    ]
  },
  {
    type: SummaryType.COUNT,
    selector: '#graph-item-count',
    isEnableKey: 'count',
    valueKey: 'count',
    maxValueFunc: (data: SummaryItem[]) =>
      d3.max(data, (d: SummaryItem) => d.task_count_total) || 0,
    valueFunc: (latest: SummaryItem) =>
      Math.floor((latest.task_count_complete / latest.task_count_total) * 100) || 0,
    list_area: [
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
  },
  {
    type: SummaryType.NUMBER,
    selector: '#graph-item-number',
    isEnableKey: 'number',
    valueKey: 'number',
    maxValueFunc: (data: SummaryItem[]) =>
      d3.max(data, (d: SummaryItem) => d.task_number_total) || 0,
    valueFunc: (latest: SummaryItem) =>
      Math.floor((latest.task_number_completed / latest.task_number_total) * 100) || 0,
    list_area: [
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
  }
]

const { is_enable, value } = useSummaryChart(props.id_project, props.rid_users, chartConfigs)
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
              <span class="value" v-if="is_enable.workload">{{ value.workload }} pt</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" id="graph-item-workload"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">completed rate</div>
            <div class="title">
              <span>Item : Workload</span>
              <span class="value" v-if="is_enable.count">{{ value.count }} %</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" id="graph-item-count"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">completed rate</div>
            <div class="title">
              <span>Item : Number</span>
              <span class="value" v-if="is_enable.number">{{ value.number }} %</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" id="graph-item-number"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
@import '@/components/analyze/summary.css';
</style>
