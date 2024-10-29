import { ref, watch } from 'vue'

import * as d3 from 'd3'

import type { SummaryItem } from '@/types/Summary'
import useProgressStore from '@/stores/ProgressStore'

export enum SummaryType {
  NONE = 0,
  WORKLOAD,
  BUG,
  RISK,
  COUNT,
  NUMBER
}

interface ChartArea {
  name: string
  value: (d: SummaryItem) => number
  color_line: string
  color_area: string
}

interface ChartConfig {
  type: SummaryType
  selector: string
  isEnableKey: string
  valueKey: string
  maxValueFunc: (data: SummaryItem[]) => number
  valueFunc: (latest: SummaryItem) => number
  list_area: ChartArea[]
}

export function useSummaryChart(
  id_project: number | null,
  rid_users: number,
  chartConfigs: ChartConfig[]
) {
  const store_progress = useProgressStore()

  const is_enable = ref<{ [key: string]: boolean }>({})
  const value = ref<{ [key: string]: number }>({})

  if (!id_project) {
    return {
      is_enable,
      value
    }
  }

  createChart(id_project, rid_users)

  watch(
    () => store_progress.rid_users,
    (value_new) => {
      createChart(id_project, value_new)
    }
  )

  async function createChart(id_project: number, rid_users: number) {
    await store_progress.fetchSummariesUser(id_project, rid_users)
    const list_data = store_progress.summaries_user.get(rid_users)
    if (!list_data || list_data.length === 0) {
      return
    }

    chartConfigs.forEach((config) => {
      const max_value = config.maxValueFunc(list_data) || 0
      is_enable.value[config.isEnableKey] = max_value !== 0

      d3.select(config.selector).selectAll('svg').remove()

      const latest = list_data[list_data.length - 1]
      value.value[config.valueKey] = config.valueFunc(latest)

      createChartDetail(config.type, list_data, max_value, config.selector, config.list_area)
    })
  }

  function createChartDetail(
    type: SummaryType,
    data: SummaryItem[],
    max_value: number,
    selector: string,
    list_area: ChartArea[]
  ) {
    const date_end = d3.max(data, (d: any) => new Date(d.date_entry)) as Date
    const date_start = new Date(date_end)
    date_start.setDate(date_end.getDate() - 21)

    const width = 260
    const height = 80

    const yDomainMax = type === SummaryType.RISK ? 1100 : max_value + 5
    const x = d3.scaleTime().domain([date_start, date_end]).range([0, width])
    const y = d3.scaleLinear().domain([0, yDomainMax]).nice().range([height, 0])

    const svg = d3
      .select(selector)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')

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

  return {
    is_enable,
    value
  }
}
