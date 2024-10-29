<script setup lang="ts">
import { defineProps } from 'vue'

// @ts-ignore
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
    selector: '#graph-bug-workload',
    isEnableKey: 'workload',
    valueKey: 'workload',
    maxValueFunc: (data: SummaryItem[]) =>
      d3.max(data, (d: SummaryItem) => Math.max(d.task_workload_total, d.bug_workload_total)) || 0,
    valueFunc: (latest: SummaryItem) => latest.bug_workload_total,
    list_area: [
      {
        name: 'Total',
        value: (d: SummaryItem) => d.bug_workload_total,
        color_line: 'rgba(180, 180, 180, 0.9)',
        color_area: 'rgba(180, 180, 180, 0.2)'
      }
    ]
  },
  {
    type: SummaryType.BUG,
    selector: '#graph-bug',
    isEnableKey: 'bug',
    valueKey: 'bug',
    maxValueFunc: (data: SummaryItem[]) => d3.max(data, (d: SummaryItem) => d.bug_count_total) || 0,
    valueFunc: (latest: SummaryItem) =>
      Math.floor((latest.bug_count_complete / latest.bug_count_total) * 100) || 0,
    list_area: [
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
  },
  {
    type: SummaryType.RISK,
    selector: '#graph-alert',
    isEnableKey: 'alert',
    valueKey: 'alert',
    maxValueFunc: (data: SummaryItem[]) =>
      d3.max(data, (d: SummaryItem) => d.task_count_alert + d.bug_count_alert) || 0,
    valueFunc: (latest: SummaryItem) => latest.task_count_alert + latest.bug_count_alert,
    list_area: [
      {
        name: 'Alert',
        value: (d: SummaryItem) => d.task_count_alert + d.bug_count_alert,
        color_line: 'rgba(181, 48, 69, 0.9)',
        color_area: 'rgba(181, 48, 69, 0.2)'
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
            <div class="graph" id="graph-bug-workload"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">completed rate</div>
            <div class="title">
              <span>Bug</span>
              <span class="value" v-if="is_enable.bug">{{ value.bug }} %</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" id="graph-bug"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto" class="d-flex summary-block">
        <v-card class="flex-grow-1" color="#000000">
          <v-card-text>
            <div class="title-sub">caution</div>
            <div class="title">
              <span>Alert</span>
              <span class="value" v-if="is_enable.alert">{{ value.alert }} alert</span>
              <span class="value" v-else>-</span>
            </div>
            <div class="graph" id="graph-alert"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
@import '@/components/analyze/summary.css';
</style>
