import { defineStore } from 'pinia'

import { ExtractType } from '@/types/Item'
import type {
  Item,
  EventCreate,
  EventUpdate,
  FeatureCreate,
  FeatureUpdate,
  StoryCreate,
  StoryUpdate,
  TaskCreate,
  TaskUpdate,
  BugCreate,
  BugUpdate
} from '@/types/Item'

import ItemService from '@/services/ItemService'
import useProjectStore from '@/stores/ProjectStore'
import useUserStore from '@/stores/UserStore'

const service_item = new ItemService()

const useItemStore = defineStore('item', {
  state: () => ({
    is_update: false as boolean,
    type_extract: ExtractType.INCOMPLETE as ExtractType,
    items: [] as Array<Item>,
    extract_rid_item: 0 as number,
    extract_search_target: '' as string
  }),
  actions: {
    updated() {
      this.is_update = false
    },
    async fetchItems(router: any) {
      this.is_update = false

      const store_user = useUserStore()
      const store_project = useProjectStore()

      const path = `/project/${store_project.selected_id_project}`

      switch (this.type_extract) {
        case ExtractType.INCOMPLETE:
          {
            this.items = await service_item.getItemsIncomplete(store_project.selected_id_project)

            const query = { extruct: this.type_extract }
            router.push({ path, query })
          }
          break

        case ExtractType.ALL:
          {
            this.items = await service_item.getItemsAll(store_project.selected_id_project)

            const query = { extruct: this.type_extract }
            router.push({ path, query })
          }
          break

        case ExtractType.HIGH_RISK:
          {
            this.items = await service_item.getItemsHighRisk(store_project.selected_id_project)

            const query = { extruct: this.type_extract }
            router.push({ path, query })
          }
          break

        case ExtractType.ALERT:
          {
            this.items = await service_item.getItemsAlert(store_project.selected_id_project)

            const query = { extruct: this.type_extract }
            router.push({ path, query })
          }
          break

        case ExtractType.ASSIGNMENT:
          {
            this.items = await service_item.getItemsAssignment(
              store_project.selected_id_project,
              store_user.login_user?.rid
            )

            const query = { extruct: this.type_extract, target: store_user.login_user?.rid }
            router.push({ path, query })
          }
          break

        case ExtractType.RELATION:
          {
            this.items = await service_item.getItemsRelation(
              store_project.selected_id_project,
              this.extract_rid_item
            )

            const query = { extruct: this.type_extract, target: this.extract_rid_item }
            router.push({ path, query })
          }
          break

        case ExtractType.SEARCH:
          {
            this.items = await service_item.getItemsSearch(
              store_project.selected_id_project,
              this.extract_search_target
            )

            const query = { extruct: this.type_extract, target: this.extract_search_target }
            router.push({ path, query })
          }
          break
      }
    },
    setExtractIncomplete() {
      this.type_extract = ExtractType.INCOMPLETE
      this.is_update = true
    },
    setExtractAll() {
      this.type_extract = ExtractType.ALL
      this.is_update = true
    },
    setExtractHighRisk() {
      this.type_extract = ExtractType.HIGH_RISK
      this.is_update = true
    },
    setExtractAlert() {
      this.type_extract = ExtractType.ALERT
      this.is_update = true
    },
    setExtractAssignment() {
      this.type_extract = ExtractType.ASSIGNMENT
      this.is_update = true
    },
    setExtractItem(rid_item: number) {
      this.type_extract = ExtractType.RELATION
      this.extract_rid_item = rid_item
      this.is_update = true
    },
    setExtractItemUpdate() {
      this.type_extract = ExtractType.RELATION
      this.is_update = true
    },
    setExtractSearch(target: string) {
      this.type_extract = ExtractType.SEARCH
      this.extract_search_target = target
      this.is_update = true
    },
    setExtractSearchUpdate() {
      this.type_extract = ExtractType.SEARCH
      this.is_update = true
    },
    async createEvent(event: EventCreate): Promise<Item> {
      const result = await service_item.createEvent(event)
      this.is_update = true
      return result
    },
    async updateEvent(event: EventUpdate): Promise<Item> {
      const result = await service_item.updateEvent(event)
      this.is_update = true
      return result
    },
    async deleteEvent(rid: number): Promise<void> {
      await service_item.deleteEvent(rid)
      this.is_update = true
    },
    async createFeature(feature: FeatureCreate): Promise<Item> {
      const result = await service_item.createFeature(feature)
      this.is_update = true
      return result
    },
    async updateFeature(feature: FeatureUpdate): Promise<Item> {
      const result = await service_item.updateFeature(feature)
      this.is_update = true
      return result
    },
    async deleteFeature(rid: number): Promise<void> {
      await service_item.deleteFeature(rid)
      this.is_update = true
    },
    async createStory(story: StoryCreate): Promise<Item> {
      const result = await service_item.createStory(story)
      this.is_update = true
      return result
    },
    async updateStory(story: StoryUpdate): Promise<Item> {
      const result = await service_item.updateStory(story)
      this.is_update = true
      return result
    },
    async deleteStory(rid: number): Promise<void> {
      await service_item.deleteStory(rid)
      this.is_update = true
    },
    async createTask(task: TaskCreate): Promise<Item> {
      const result = await service_item.createTask(task)
      this.is_update = true
      return result
    },
    async updateTask(task: TaskUpdate): Promise<Item> {
      const result = await service_item.updateTask(task)
      this.is_update = true
      return result
    },
    async deleteTask(rid: number): Promise<void> {
      await service_item.deleteTask(rid)
      this.is_update = true
    },
    async createBug(bug: BugCreate): Promise<Item> {
      const result = await service_item.createBug(bug)
      this.is_update = true
      return result
    },
    async updateBug(bug: BugUpdate): Promise<Item> {
      const result = await service_item.updateBug(bug)
      this.is_update = true
      return result
    },
    async deleteBug(rid: number): Promise<void> {
      await service_item.deleteBug(rid)
      this.is_update = true
    }
  }
})

export default useItemStore
