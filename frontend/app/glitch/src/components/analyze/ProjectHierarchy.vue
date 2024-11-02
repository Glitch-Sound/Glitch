<script setup lang="ts">
import { onMounted } from 'vue'

import * as d3 from 'd3'

import useProgressStore from '@/stores/ProgressStore'

const props = defineProps<{
  id_project: number | null
}>()

const store_progress = useProgressStore()

onMounted(async () => {
  await store_progress.fetchHierarchy(props.id_project)
  createSunburstChart()
})

interface HierarchyData {
  rid: number
  rid_users: number
  name: string
  title: string
  workload_task?: number
  workload_bug?: number
  children?: HierarchyData[]
}

function createSunburstChart() {
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

  const colors = ['#efbf4d', '#9c357c', '#028c06']
  const color_task = '#4169e1'
  const color_bug = '#cd0000'

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
    .style('stroke-width', 1.5)
    .style('fill-opacity', () => 0.8)
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
