<script setup lang="ts">
import { onMounted, watch } from 'vue'

import * as d3 from 'd3'

import useProgressStore from '@/stores/ProgressStore'

const props = defineProps<{
  id_project: number | null
  rid_users: number
}>()

const store_progress = useProgressStore()

onMounted(async () => {
  await store_progress.fetchHierarchy(props.id_project)
  createSunburstChart(props.rid_users)
})

watch(
  () => store_progress.rid_users,
  (value_new) => {
    d3.select(`#sunburst`).selectAll('svg').remove()
    createSunburstChart(value_new)
  }
)

interface HierarchyData {
  rid: number
  rid_users: number
  name: string
  title: string
  workload_task?: number
  workload_bug?: number
  children?: HierarchyData[]
}

function createSunburstChart(rid_users: number) {
  const width = 350
  const radius = 150
  const radius_ratio_inncer = 0.6
  const partition = d3
    .partition<HierarchyData>()
    .size([2 * Math.PI, radius * (1 - radius_ratio_inncer)])

  const root = d3
    .hierarchy<HierarchyData>(store_progress.hierarchy as HierarchyData)
    .sum((d: HierarchyData) => (d.workload_task || 0) + (d.workload_bug || 0))
    .sort((a: d3.HierarchyNode<HierarchyData>, b: d3.HierarchyNode<HierarchyData>) => {
      return (b.value || 0) - (a.value || 0)
    })

  partition(root)

  const svg = d3
    .select('#sunburst')
    .append('svg')
    .attr('width', width)
    .attr('height', width)
    .append('g')
    .attr('transform', `translate(${width / 2},${width / 2})`)

  const arc = d3
    .arc()
    .startAngle((d: any) => d.x0)
    .endAngle((d: any) => d.x1)
    .innerRadius((d: any) => (d.depth === 0 ? 0 : radius * radius_ratio_inncer + d.y0))
    .outerRadius((d: any) => radius * radius_ratio_inncer + d.y1)
    .cornerRadius(2)

  const colors = ['#efbf4d', '#b34b92', '#028c06']
  const color_task = '#4169e1'
  const color_bug = '#a80000'

  const max_depth = Math.max(...root.descendants().map((d: any) => d.depth))

  svg
    .selectAll('path')
    .data(root.descendants())
    .enter()
    .append('path')
    .attr('d', arc as any)
    .style('fill', (d: any) => {
      if (d.depth === 0) {
        return '#000000'
      } else if (d.depth === 4) {
        if (0 < d.data.workload_task) {
          return color_task
        } else {
          return color_bug
        }
      } else if (d.depth <= max_depth && d.depth < 4) {
        return colors[d.depth - 1]
      }
      return '#000000'
    })
    .style('stroke', '#101010')
    .style('stroke-width', 2.0)
    .style('fill-opacity', (d: any) => (d.data.rid_users === rid_users ? 0.9 : 0.3))
}
</script>

<template>
  <v-container class="summary">
    <div id="sunburst"></div>
  </v-container>
</template>

<style scoped>
.summary {
  margin: 0 25px 0 50px;
  padding: 0;
}
</style>
