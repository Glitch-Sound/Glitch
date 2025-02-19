<script setup lang="ts">
import { TaskType, type Item, type TaskCreate } from '@/types/Item'
import type { User } from '@/types/User'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import useUserStore from '@/stores/UserStore'
import useProjectStore from '@/stores/ProjectStore'
import UserSelect from '@/components/common/UserSelect.vue'
import WorkloadSelect from '@/components/common/WorkloadSelect.vue'

const store_user = useUserStore()
const store_project = useProjectStore()

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, submitData } = useFormDialog<TaskCreate>(emit)

defineExpose({
  open(item_parent: Item) {
    dialog.value = true
    form_data.value = {
      id_project: store_project.selected_id_project,
      rid_items: item_parent.rid,
      rid_users: store_user.login_user?.rid ?? 0,
      title: '',
      detail: '',
      task_type: TaskType.WORKLOAD,
      task_workload: 0,
      task_number_completed: 0,
      task_number_total: 0
    }
  },
  close() {
    dialog.value = false
  }
})

const handleUserSelected = (user: User) => {
  form_data.value.rid_users = user.rid
}

const handleWorkloadSelect = (workload: number) => {
  form_data.value.task_workload = workload
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1300px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add Task</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <UserSelect v-model="form_data.rid_users" @itemSelected="handleUserSelected" />

          <v-text-field
            v-model="form_data.title"
            :rules="[rules.required]"
            label="Title"
            required
          />

          <v-textarea v-model="form_data.detail" label="Detail" />

          <div class="mb-4 text-center">
            <v-btn-toggle v-model="form_data.task_type" mandatory>
              <v-btn :value="TaskType.WORKLOAD">Workload</v-btn>
              <v-btn :value="TaskType.NUMBER">Number</v-btn>
            </v-btn-toggle>
          </div>

          <WorkloadSelect
            v-if="form_data.task_type == TaskType.WORKLOAD"
            :workload="null"
            @itemSelected="handleWorkloadSelect"
          />

          <v-text-field
            v-if="form_data.task_type == TaskType.NUMBER"
            v-model="form_data.task_number_completed"
            label="Number completed"
          />

          <v-text-field
            v-if="form_data.task_type == TaskType.NUMBER"
            v-model="form_data.task_number_total"
            :rules="[rules.required]"
            label="Number total"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="submitData">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
