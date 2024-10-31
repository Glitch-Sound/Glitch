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

export enum RiskType {
  NONE = 0,
  LIMIT = 1,
  OVER = 2
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

export interface ItemRange {
  rid: number
  type: number
  state: number
  title: string
  datetime_start: string
  datetime_end: string
}

export interface StateUpdate {
  rid: number
  state: number
}

export interface Project {
  rid: number
  id_project: number
  state: number
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
  project_datetime_start: string
  project_datetime_end: string
}

export interface ProjectUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  project_datetime_start: string
  project_datetime_end: string
}

export interface EventCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  event_datetime_end: string
}

export interface EventUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  event_datetime_end: string
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
  story_datetime_start: string
  story_datetime_end: string
}

export interface StoryUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  story_datetime_start: string
  story_datetime_end: string
}

export interface TaskCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  task_type: number
  task_workload: number
  task_number_completed: number
  task_number_total: number
}

export interface TaskUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  task_type: number
  task_workload: number
  task_number_completed: number
  task_number_total: number
}

export interface TaskPriorityUpdate {
  rid: number
  priority: number
}

export interface BugCreate {
  id_project: number
  rid_items: number
  rid_users: number
  title: string
  detail: string
  bug_workload: number
}

export interface BugUpdate {
  rid: number
  state: number
  rid_users: number
  rid_users_review: number | null
  title: string
  detail: string
  result: string
  bug_workload: number
}

export interface BugPriorityUpdate {
  rid: number
  priority: number
}

export interface ItemHierarchy {
  rid: number
  rid_users: number
  name: string
  title: string
  workload_task?: number
  workload_bug?: number
  children?: ItemHierarchy[]
}
