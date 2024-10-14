import { defineStore } from 'pinia'

import type { Item, Project, ProjectCreate, ProjectUpdate } from '@/types/Item'
import ItemService from '@/services/ItemService'

const service_item = new ItemService()

const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [] as Array<Project>,
    selected_id_project: 0 as number
  }),
  actions: {
    async fetchProjects() {
      this.projects = await service_item.getProjects()
    },
    setSelectedProjectID(id_project: number | null) {
      if (id_project) {
        this.selected_id_project = id_project
      }
    },
    async createProject(project: ProjectCreate): Promise<Item> {
      const result = await service_item.createProject(project)
      await this.fetchProjects()
      return result
    },
    async updateProject(project: ProjectUpdate): Promise<Item> {
      const result = await service_item.updateProject(project)
      await this.fetchProjects()
      return result
    },
    async deleteProject(rid: number): Promise<void> {
      await service_item.deleteProject(rid)
      await this.fetchProjects()
    }
  }
})

export default useProjectStore
