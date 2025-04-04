import { defineStore } from 'pinia'

import type { Item, ItemHierarchy } from '@/types/Item'
import type { SummaryItem } from '@/types/Summary'

import ItemService from '@/services/ItemService'
import SummaryService from '@/services/SummaryService'

const service_item = new ItemService()
const service_summary = new SummaryService()

const useAnalyzeStore = defineStore('analyze', {
  state: () => ({
    items: [] as Array<Item>,
    summaries_project: [] as Array<SummaryItem>,
    hierarchy: null as ItemHierarchy | null
  }),
  actions: {
    async fetchItems(id_project: number | null) {
      this.items = await service_item.getItemsNotice(id_project)
    },
    async fetchSummaryProject(id_project: number | null) {
      if (id_project) {
        this.summaries_project = await service_summary.getSummariesProject(id_project)
      }
    },
    async fetchHierarchy(id_project: number | null) {
      this.hierarchy = await service_item.getHierarchy(id_project)
    }
  }
})

export default useAnalyzeStore
