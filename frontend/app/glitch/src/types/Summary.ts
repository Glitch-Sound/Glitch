export interface SummaryItem {
  rid: number
  id_project: number
  risk: number
  task_count_idle: number
  task_count_run: number
  task_count_alert: number
  task_count_review: number
  task_count_complete: number
  task_count_total: number
  task_workload_total: number
  task_number_completed: number
  task_number_total: number
  bug_count_idle: number
  bug_count_run: number
  bug_count_alert: number
  bug_count_review: number
  bug_count_complete: number
  bug_count_total: number
  bug_workload_total: number
  date_entry: string
}

export interface SummaryUser {
  rid: number
  id_project: number
  rid_users: number
  name: string
  risk: number
  task_count_idle: number
  task_count_run: number
  task_count_alert: number
  task_count_review: number
  task_count_complete: number
  task_count_total: number
  task_workload_total: number
  task_number_completed: number
  task_number_total: number
  bug_count_idle: number
  bug_count_run: number
  bug_count_alert: number
  bug_count_review: number
  bug_count_complete: number
  bug_count_total: number
  bug_workload_total: number
  date_entry: string
}
