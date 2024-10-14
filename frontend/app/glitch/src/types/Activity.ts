export interface Activity {
  rid: number
  activity: string
  datetime_entry: string
  datetime_update: string
  rid_users: number
  name: string
}

export interface ActivityCreate {
  rid_items: number
  rid_users: number
  activity: string
}

export interface ActivityUpdate {
  rid: number
  activity: string
}
