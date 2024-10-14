import http from '@/services/ApiClient'

import type { SummaryItem, SummaryUser } from '@/types/Summary'

class SummaryService {
  public async getSummariesProject(id_project: number): Promise<SummaryItem[]> {
    try {
      const response = await http.get<SummaryItem[]>(`/api/summary/project/${id_project}`)
      return response.data
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }

  public async getSummariesItem(rid_items: number): Promise<SummaryItem[]> {
    try {
      const response = await http.get<SummaryItem[]>(`/api/summary/item/${rid_items}`)
      return response.data
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }

  public async getSummariesUser(id_project: number, rid_users: number): Promise<SummaryUser[]> {
    try {
      const response = await http.get<SummaryUser[]>(`/api/summary/user/${id_project}/${rid_users}`)
      return response.data
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }
}

export default SummaryService
