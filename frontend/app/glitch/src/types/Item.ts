export enum ItemType {
  NONE = 0,
  PROJECT,
  EVENT,
  FEATURE,
  STORY,
  TASK,
  BUG
}

export enum ItemState {
  NONE = 0,
  IDLE,
  RUN,
  ALERT,
  REVIEW,
  COMPLETE
}

export enum TaskType {
  NONE = 0,
  WORKLOAD,
  NUMBER
}

export enum WorkloadType {
  NONE = 0,
  WITHIN_AN_HOUR = 1,
  WITHIN_HALF_A_DAY = 3,
  WITHIN_A_DAY = 7,
  WITHIN_2_DAYS = 14,
  WITHIN_3_DAYS = 21,
  WITHIN_A_WEEK = 35
}

export enum ExtractType {
  NONE = 0,
  INCOMPLETE,
  ALL,
  HIGH_RISK,
  ALERT,
  ASSIGNMENT,
  RELATION,
  SEARCH
}

export interface PanelRelation {
  is_top: boolean
  is_bottom: boolean
  has_child: boolean
  is_exist_next_event: boolean
  is_exist_next_feature: boolean
  is_exist_next_story: boolean
  is_exist_next_task_bug: boolean
}

export interface RID {
  rid: number
}

export interface Item {
  rid: number
  id_project: number
  type: ItemType
  state: ItemState
  risk: number
  risk_factors: number
  priority: number
  title: string
  detail: string
  result: string
  datetime_entry: string
  datetime_update: string
  rid_users: number
  name: string
  rid_users_review: number | null
  name_review: string | null
  project_datetime_start: string
  project_datetime_end: string
  event_datetime_end: string
  story_datetime_start: string
  story_datetime_end: string
  task_type: TaskType
  task_workload: number
  task_number_completed: number
  task_number_total: number
  bug_workload: number
}

export interface Project {
  rid: number
  id_project: number
  state: number
  risk: number
  title: string
  detail: string
  result: string
  datetime_entry: string
  datetime_update: string
  rid_users: number
  name: string
  project_datetime_start: string
  project_datetime_end: string
}

export interface ProjectCreate {
  rid_users: number
  title: string
  detail: string
  datetime_start: string
  datetime_end: string
}

export interface ProjectUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  datetime_start: string
  datetime_end: string
}

export interface EventCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  datetime_end: string
}

export interface EventUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  datetime_end: string
}

export interface FeatureCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
}

export interface FeatureUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
}

export interface StoryCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  datetime_start: string
  datetime_end: string
}

export interface StoryUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  datetime_start: string
  datetime_end: string
}

export interface TaskCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  type: number
  workload: number
  number_completed: number
  number_total: number
}

export interface TaskUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  type: number
  workload: number
  number_completed: number
  number_total: number
}

export interface BugCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  workload: number
}

export interface BugUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  workload: number
}
