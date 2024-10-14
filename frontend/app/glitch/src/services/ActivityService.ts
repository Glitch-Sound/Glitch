import http from '@/services/ApiClient'

import type { Activity, ActivityCreate, ActivityUpdate } from '@/types/Activity'

class ActivityService {
  public async getActivities(rid_items: number): Promise<Activity[]> {
    try {
      const response = await http.get<Activity[]>(`/api/activity/${rid_items}`)
      return response.data
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }

  public async createActivity(activity: ActivityCreate): Promise<Activity> {
    try {
      const response = await http.post<Activity>('/api/activity', activity)
      return response.data
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }

  public async updateActivity(activity: ActivityUpdate): Promise<Activity> {
    try {
      const response = await http.put<Activity>('/api/activity', activity)
      return response.data
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }

  public async deleteActivity(rid: number): Promise<void> {
    try {
      await http.delete(`/api/project/${rid}`)
    } catch (error) {
      console.trace()
      throw new Error('error: ${error}')
    }
  }
}

export default ActivityService
