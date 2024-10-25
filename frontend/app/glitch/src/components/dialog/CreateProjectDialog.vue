<script setup lang="ts">
import { defineExpose, ref, watch } from 'vue'

import type { ProjectCreate } from '@/types/Item'
import type { User } from '@/types/User'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import useUserStore from '@/stores/UserStore'
import UserSelect from '@/components/common/UserSelect.vue'

const store_user = useUserStore()

const date_min = ref('')
const date_max = ref('')

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, submitData } = useFormDialog<ProjectCreate>(emit)

watch(
  () => form_data.value.datetime_start,
  (datetime_start) => {
    date_min.value = datetime_start
  }
)

watch(
  () => form_data.value.datetime_end,
  (datetime_end) => {
    date_max.value = datetime_end
  }
)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      rid_users: store_user.login_user?.rid ?? 0,
      title: '',
      detail: '',
      datetime_start: '',
      datetime_end: ''
    }
  },
  close() {
    dialog.value = false
  }
})

const handleUserSelected = (user: User) => {
  form_data.value.rid_users = user.rid
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1300px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add Project</span>
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

          <v-text-field
            class="dialog-field"
            v-model="form_data.datetime_start"
            :rules="[rules.required]"
            label="Start"
            type="date"
            required
            :max="date_max"
          />

          <v-text-field
            class="dialog-field"
            v-model="form_data.datetime_end"
            :rules="[rules.required]"
            label="End"
            type="date"
            required
            :min="date_min"
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
