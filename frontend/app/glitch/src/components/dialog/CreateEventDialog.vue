<script setup lang="ts">
import { defineExpose } from 'vue'

import type { EventCreate } from '@/types/Item'
import type { User } from '@/types/User'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import useUserStore from '@/stores/UserStore'
import useProjectStore from '@/stores/ProjectStore'
import UserSelect from '@/components/common/UserSelect.vue'

const store_user = useUserStore()
const store_project = useProjectStore()

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, submitData } = useFormDialog<EventCreate>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      id_project: store_project.selected_id_project,
      rid_items: store_project.selected_id_project,
      rid_users: store_user.login_user?.rid ?? 0,
      title: '',
      detail: '',
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
        <span class="dialog-title">Add Event</span>
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
            v-model="form_data.datetime_end"
            :rules="[rules.required]"
            label="End"
            type="date"
            required
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
