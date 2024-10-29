import { defineStore } from 'pinia'

import type { User } from '@/types/User'
import type { Item, ItemHierarchy } from '@/types/Item'
import type { SummaryUser } from '@/types/Summary'

import ItemService from '@/services/ItemService'
import UserService from '@/services/UserService'
import SummaryService from '@/services/SummaryService'
import useItemStore from '@/stores/ItemStore'

const service_user = new UserService()
const service_item = new ItemService()
const service_summary = new SummaryService()

const useProgressStore = defineStore('progress', {
  state: () => ({
    items: [] as Array<Item>,
    users: [] as Array<User>,
    hierarchy: null as ItemHierarchy | null,
    rid_users: 0 as number,
    summaries_user: new Map<number, Array<SummaryUser>>()
  }),
  actions: {
    async fetchItems(id_project: number, rid_users: number) {
      const service_item = new ItemService()
      this.items = await service_item.getItemsSummaryUser(id_project, rid_users)

      const store_item = useItemStore()
      store_item.updated()
    },
    async fetchUsers(id_project: number) {
      this.users = await service_user.getUsersProject(id_project)
    },
    async fetchHierarchy(id_project: number | null) {
      this.hierarchy = await service_item.getHierarchy(id_project)
    },
    setUser(rid_users: number) {
      this.rid_users = rid_users
    },
    async fetchSummariesUser(id_project: number, rid_users: number) {
      const summaries = await service_summary.getSummariesUser(id_project, rid_users)
      this.summaries_user.set(rid_users, summaries)
    }
  }
})

export default useProgressStore
